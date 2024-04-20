from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from polls.models import Survey, SmsConversation, SMS, SMSReceived, Account, SurveyResponse, SurveyQuestion
from polls.sentiment_analysis.service import SentimentAnalysisService

class SentimentAnalysisServiceTest(TestCase):
    def setUp(self):
        # Create any necessary objects for testing, like survey questions, SMS, etc.
        pass

    def test_analyze_sentiment_positive(self):
        # Create a sentiment analysis service instance
        sentiment_service = SentimentAnalysisService()

        # Test a positive sentiment
        sentiment = sentiment_service.analyze_sentiment("I love this product!")
        self.assertEqual(sentiment, SurveyResponse.POSITIVE)

    def test_analyze_sentiment_negative(self):
        # Create a sentiment analysis service instance
        sentiment_service = SentimentAnalysisService()

        # Test a negative sentiment
        sentiment = sentiment_service.analyze_sentiment("I hate this product!")
        self.assertEqual(sentiment, SurveyResponse.NEGATIVE)

    # Add more test cases as needed...

    def tearDown(self):
        # Clean up any objects created during testing
        pass
