from ...models import Survey, SmsConversation, SMS, SMSReceived, Account, SurveyResponse, SurveyQuestion
from nltk.sentiment import SentimentIntensityAnalyzer
import re
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
import nltk
class SentimentAnalysisService:
    def __init__(self):
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('stopwords')
        self.analyzer = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):
        # Remove special characters and convert to lower case
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return cleaned_text.lower()


    def analyze_sentiment_on_survey_response(self, sms_list, current_sms: SMS, sms_conversation: SmsConversation, survey_question: SurveyQuestion):
        current_sms_clean = self.clean_text(current_sms.message)
        current_sms_sentiment = self.analyze_sentiment(current_sms_clean)
        current_sms_aspects = self.extract_aspects(current_sms_clean)

        # Save additional information to the database
        sms_response = self.save_additional_info(survey_question, current_sms_clean, current_sms_sentiment, current_sms_aspects)

        return sms_response

    def analyze_sentiment(self, text):
        score = self.analyzer.polarity_scores(text)['compound']
        if score > 0.05:
            return SurveyResponse.POSITIVE
        elif score < -0.05:
            return SurveyResponse.NEGATIVE
        else:
            return SurveyResponse.NEUTRAL

    def extract_aspects(self, text):
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_words]
        tagged_tokens = pos_tag(tokens)
        nouns = [word for word, tag in tagged_tokens if tag.startswith("NN")]
        return ", ".join(nouns)

    def save_additional_info(self, survey_question, full_response, sentiment, aspects):
        response = None
        # Implement database interaction for saving additional information
        try:
            response = SurveyResponse.objects.create(
                survey_question=survey_question,
                response_body=full_response,
                sentiment=sentiment,
                aspects=aspects
            )
            response.save()
            print("Additional information saved successfully.")
        except Exception as e:
            print(f"Failed to save additional information: {e}")

        return response
