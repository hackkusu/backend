from ...models import Survey, Conversation, SMS, SMSReceived, Account, SurveyResponse, SurveyQuestion, SMSSent, \
    SmsConversation
import os
from twilio.rest import Client
from twilio.request_validator import RequestValidator
from ..sentiment_analysis.service import SentimentAnalysisService

class TwilioService:
    @staticmethod
    def send_mms(account: Account, to_number: str, from_number: str, body: str, media_url: str):
        client = Client(account.twilio_account_sid, account.twilio_auth_token)
        message = client.messages \
            .create(
            body=body,
            from_=from_number,
            media_url=[media_url],
            to=to_number
        )
        return message

    @staticmethod
    def process_inbound_message(data=None):
        # lookup account
        account = Account.objects.filter(twilio_account_sid=data.get('AccountSid')).first()

        if not account:
            raise Exception('Account not found')

        # save sms received
        sms = SMS(from_number=data.get('From'), to_number=data.get('To'), twilio_sid=data.get('MessageSid'), message=data.get('Body'), account=account)
        sms.save()
        sms_received = SMSReceived(sms=sms)
        sms_received.save()

        # todo: check if it is a stop word
        # Handle stop words
        stop_words = ['STOP', 'END', 'CANCEL', 'UNSUBSCRIBE']  # Define stop words
        if data.get('Body').strip().upper() in stop_words:
            # TODO: handle the stop request
            # For example, mark the conversation as stopped, or unsubscribe the user
            pass

        response_msg = None

        # # Check if it is a start code from an existing campaign
        # start_code = data.get('Body').strip()
        # new_survey = Survey.objects.filter(phone__number=data.get('To'), start_code__iexact=start_code).first()


        # todo: check existing conversation
        conversation: Conversation = Conversation.objects.filter(phone_number=data.get('From'), survery__phone__number=data.get('To'), closed=False).first()



        if not conversation:
            # todo: check if text is keyword from existing campaign
            new_survey = Survey.objects.filter(phone__number=data.get('To'), start_code__iexact=data.get('Body').strip()).first()

            if new_survey is not None:
                conversation = Conversation(survery=new_survey, last_sms=sms, phone_number=data.get('From'))
                conversation.save()

                # new survey first question
                next_survey_question: SurveyQuestion = conversation.survery.survey_questions.filter(
                    sort_order=0).first()
                conversation.last_survey_question = next_survey_question
                conversation.save()

                TwilioService.send_outgoing_sms(account,
                                                next_survey_question.question,
                                                data.get('To'), data.get('From'))

                return TwilioService.send_outgoing_sms(account, "Text in as many times as you'd like then send \"done\" by itself when you are finished with each response.", data.get('To'), data.get('From'))
                # send text as many times as you'd like and send done by itself when complete
            else:
                return TwilioService.send_outgoing_sms(account,
                                                       'To start a survey, please text us the unique START code you received. Text STOP to be permanetely unsubscribed.',
                                                       data.get('To'), data.get('From'))

        if conversation is not None:

            # TODO: Check if the user wants to end the survey, e.g., by looking for 'DONE' in the response
            if 'DONE' in data.get('Body').strip().upper():
                # end_survey(sms_conversation)

                if conversation.last_survey_question_id is not None:
                    next_survey_question: SurveyQuestion = conversation.survery.survey_questions.filter(sort_order=conversation.last_survey_question.sort_order + 1).first()

                    if next_survey_question is not None:
                        response_msg = next_survey_question.question
                        conversation.last_survey_question = next_survey_question
                        conversation.save()
                    else:
                        response_msg = 'Thank you for completing the survey!'
                        conversation.closed = True
                        conversation.save()

                else:
                    # new survey first question todo: is this needed?
                    next_survey_question: SurveyQuestion = conversation.survery.survey_questions.filter(sort_order=0).first()
                    conversation.last_survey_question = next_survey_question
                    conversation.save()


            # todo: sentiment analysis and save survey response



                # survey_response = SurveyResponse()
                service = SentimentAnalysisService()
                service.analyze_sentiment_on_survey_response(list(SMS.objects.all()), sms, conversation)


                # todo: decide what to text them back
                # response_msg = next_survey_question.question


                # Find your Account SID and Auth Token at twilio.com/console
                # and set the environment variables. See http://twil.io/secure
                # account_sid = os.environ['TWILIO_ACCOUNT_SID']
                # auth_token = os.environ['TWILIO_AUTH_TOKEN']

                return TwilioService.send_outgoing_sms(account, response_msg, data.get('To'), data.get('From'))
            else:
                sms_conversation = SmsConversation(sms=sms, conversation=conversation)
                sms_conversation.save()

    @staticmethod
    def send_outgoing_sms(account: Account, msg, from_twilio_number, to_phone_number):
        client = Client(account.twilio_account_sid, account.twilio_auth_token)

        message = client.messages \
            .create(
            body=msg,
            from_=from_twilio_number,
            to=to_phone_number
        )

        # save sms received
        sms_out = SMS(from_number=from_twilio_number, to_number=to_phone_number,
                      message=msg, account=account, twilio_sid=message.sid)
        sms_out.save()
        sms_sent = SMSSent(sms=sms_out)
        sms_sent.save()

        print(message.sid)

        return message
