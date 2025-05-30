from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.diary.models import Diary
from apps.account.models import User
from bson import ObjectId

class Command(BaseCommand):
    help = 'Initialize diary data to MongoDB, specify username or user token'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Specify username')
        parser.add_argument('--token', type=str, help='Specify user token (_id)')

    def handle(self, *args, **options):
        try:
            user = None
            if options['token']:
                user = User.objects.get(_id=ObjectId(options['token']))
                self.stdout.write(self.style.SUCCESS(f'User found by token: {user.username}'))
            elif options['username']:
                user = User.objects.get(username=options['username'])
                self.stdout.write(self.style.SUCCESS(f'User found by username: {user.username}'))
            else:
                self.stdout.write(self.style.ERROR('Please specify a user by --username or --token'))
                return

            # Example diary content
            diary_contents = [
                {
                    'content': 'Today was a wonderful day! I went for a walk in the park with friends, the sun was shining, and I felt full of energy. Watching children play made me especially happy.',
                    'emotion': 'happy',
                    'intensity': 8
                },
                {
                    'content': 'Work pressure is a bit high, the project deadline is approaching, and I feel somewhat anxious. Need to adjust my mindset and plan my time better.',
                    'emotion': 'neutral',
                    'intensity': 6
                },
                {
                    'content': 'Today was peaceful, I completed my work as usual, read a book during lunch break, and felt that the pace of life was just right.',
                    'emotion': 'neutral',
                    'intensity': 5
                },
                {
                    'content': 'Had a video call with family, heard that grandma is not feeling well, which made me a bit sad. Hope she recovers soon.',
                    'emotion': 'sad',
                    'intensity': 7
                },
                {
                    'content': 'Received the long-awaited offer! So happy! All the hard work finally paid off, I feel like I\'m glowing!',
                    'emotion': 'happy',
                    'intensity': 9
                },
                {
                    'content': 'Been working overtime for three days straight, feeling physically and mentally exhausted. Need to rest and adjust my state.',
                    'emotion': 'neutral',
                    'intensity': 7
                },
                {
                    'content': 'Met a very rude person on the subway who cut in line and glared at me, it really made me angry. Deep breaths, don\'t let such people affect me.',
                    'emotion': 'angry',
                    'intensity': 6
                }
            ]

            # Clear existing test data
            Diary.objects.filter(user=user).delete()
            self.stdout.write(self.style.SUCCESS('Cleared existing data'))

            # Insert new diary data
            for i, content_data in enumerate(diary_contents):
                date = timezone.now() - timedelta(days=i)
                diary = Diary.objects.create(
                    user=user,
                    content=content_data['content'],
                    emotion_type=content_data['emotion'],
                    emotion_intensity=content_data['intensity'],
                    created_at=date
                )
                self.stdout.write(self.style.SUCCESS(f'Inserted diary entry {i+1}'))

            self.stdout.write(self.style.SUCCESS(f'Successfully created sample diary data for user {user.username}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to initialize data: {str(e)}'))