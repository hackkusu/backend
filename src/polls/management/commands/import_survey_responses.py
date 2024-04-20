from django.core.management.base import BaseCommand, CommandError
from polls.models import SurveyResponse, SurveyQuestion  # adjust 'polls' to your app name
import csv
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Loads data from a CSV file into the SurveyResponse model.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        file_path = options['csv_file']
        try:
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    created_time = parse_datetime(row['created'])
                    response = SurveyResponse(
                        id=int(row['id']),
                        created=created_time,
                        response_body=row['response_body'],
                        sentiment=row['sentiment'],
                        survey_question_id=int(row['survey_question_id']),
                        aspects=row['aspects'] if row['aspects'] != 'none' else ''
                    )
                    response.save()
            self.stdout.write(self.style.SUCCESS('Successfully loaded data into database.'))
        except Exception as e:
            raise CommandError('Failed to load data from "{}": {}'.format(file_path, e))
