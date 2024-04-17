from ...models import Survey, SmsConversation, SMS, SMSReceived, Account, SurveyResponse, SurveyQuestion
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

        # todo: check existing conversation
        sms_conversation: SmsConversation = SmsConversation.objects.filter(phone_number=data.get('From'), survery__phone__number=data.get('To')).first()

        if not sms_conversation:
            # todo: check if text is keyword from existing campaign
            new_survey = Survey.objects.filter(phone__number=data.get('To'), start_code__iexact=data.get('Body')).first()

            if new_survey is not None:
                sms_conversation = SmsConversation(survery=new_survey, last_sms=sms, phone_number=data.get('From'))
                sms_conversation.save()

        if sms_conversation is not None:
            if sms_conversation.last_survey_question_id is not None:
                next_survey_question: SurveyQuestion = sms_conversation.survery.survey_questions.filter(sort_order=sms_conversation.last_survey_question.sort_order + 1).first()

                if next_survey_question is None:
                    next_survey_question = sms_conversation.survery.survey_questions.filter(sort_order=sms_conversation.last_survey_question.sort_order).first()

                sms_conversation.last_survey_question = next_survey_question
                sms_conversation.save()
            else:
                next_survey_question: SurveyQuestion = sms_conversation.survery.survey_questions.filter(sort_order=0).first()
                sms_conversation.last_survey_question = next_survey_question
                sms_conversation.save()


            # todo: sentiment analysis and save survey response

            # survey_response = SurveyResponse()
            service = SentimentAnalysisService()
            service.analyze_sentiment_on_survey_response(list(SMS.objects.all()), sms, sms_conversation, next_survey_question)


            # todo: decide what to text them back
            response_msg = next_survey_question.question


            # Find your Account SID and Auth Token at twilio.com/console
            # and set the environment variables. See http://twil.io/secure
            # account_sid = os.environ['TWILIO_ACCOUNT_SID']
            # auth_token = os.environ['TWILIO_AUTH_TOKEN']
            client = Client(account.twilio_account_sid, account.twilio_auth_token)

            message = client.messages \
                .create(
                body=response_msg,
                from_=data.get('To'),
                to=data.get('From')
            )

            print(message.sid)


        # todo: record responses
        pass
