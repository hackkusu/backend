from ...models import Survey, SmsConversation, SMS, SMSReceived, Account, SurveyResponse, SurveyQuestion
from nltk.sentiment import SentimentIntensityAnalyzer
import re
from nltk.tokenize import word_tokenize, pos_tag
from nltk.corpus import stopwords
import nltk
class SentimentAnalysisService:
    def __init__(self):
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        self.analyzer = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):
        # Remove special characters and convert to lower case
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return cleaned_text.lower()

    def analyze_sentiment_on_survey_response(self, sms_list, sms: SMS, sms_conversation: SmsConversation, survey_question: SurveyQuestion):
        sentiment_response = sms_list[0].body if len(sms_list) > 0 else ""
        aspect_response = sms_list[1].body if len(sms_list) > 1 else ""
        additional_information = sms_list[2].body if len(sms_list) > 2 else ""

        # Clean responses
        sentiment_response_clean = self.clean_text(sentiment_response)
        aspect_response_clean = self.clean_text(aspect_response)

        # Analyze sentiment
        sentiment = self.analyze_sentiment(sentiment_response_clean)

        # Extract aspects
        aspects = self.extract_aspects(aspect_response_clean)

        # Save additional information to the database
        self.save_additional_info(survey_question, additional_information, sentiment)

        return sentiment, aspects

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

    def save_additional_info(self, survey_question, info, sentiment):
        # Implement database interaction for saving additional information
        try:
            response = SurveyResponse.objects.create(
                survey_question=survey_question,
                response_body=info,
                sentiment=sentiment
            )
            response.save()
            print("Additional information saved successfully.")
        except Exception as e:
            print(f"Failed to save additional information: {e}")
