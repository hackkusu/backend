from ...models import Survey, SmsConversation, SMS, SMSReceived


class TwilioService:
    @staticmethod
    def process_inbound_message(data=None):
        # save sms received
        sms = SMS(from_number=data.get('From'), to_number=data.get('To'), twilio_sid=data.get('MessageSid'), message=data.get('Body'))
        sms.save()
        sms_received = SMSReceived(sms=sms)
        sms_received.save()

        # todo: check if it is a stop word

        # todo: check if text is keyword from existing campaign
        survey = Survey.objects.filter(phone__number=data.get('To'), start_code__iexact=data.get('Body')).first()

        if survey is not None:
            sms_conversation = SmsConversation(survery=survey, last_sms=sms, phone_number=data.get('From'))
            sms_conversation.save()

        # todo: check if ongoing conversation
        sms_conversation: SmsConversation = SmsConversation.objects.filter(phone_number=data.get('From')).first()

        if sms_conversation is not None:
            if sms_conversation.last_survey_question_id is not None:
                next_survey_question = sms_conversation.survery.survey_questions.filter(sort_order=sms_conversation.last_survey_question.sort_order + 1).first()
            else:
                next_survey_question = sms_conversation.survery.survey_questions.filter(sort_order=0).first()

            # todo: sentiment analysis and save survey response



        # todo: decide what to text them back


        # todo: record responses
        pass


