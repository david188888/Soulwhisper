from django.core.management.base import BaseCommand
from apps.community.models import DailyKeyword, HealingQuote, HealingActivity
from django.utils import timezone

class Command(BaseCommand):
    help = 'Initialize daily content data (keywords, quotes, activities)'

    def handle(self, *args, **options):
        try:
            # Initialize daily keywords
            keywords = [
                {
                    'keyword': 'Gratitude',
                    'description': 'Be thankful for every beautiful moment in life and cherish what you have.'
                },
                {
                    'keyword': 'Courage',
                    'description': 'Stay brave in the face of difficulties and believe in your ability to overcome challenges.'
                },
                {
                    'keyword': 'Hope',
                    'description': 'Keep hope alive, believe tomorrow will be better, and the future is full of possibilities.'
                },
                {
                    'keyword': 'Calm',
                    'description': 'Find inner peace in the midst of noise and learn to be alone with yourself.'
                },
                {
                    'keyword': 'Growth',
                    'description': 'Treat every experience as an opportunity to grow, keep learning and improving.'
                }
            ]

            # Initialize healing quotes
            quotes = [
                {
                    'content': 'You deserve to be treated gently, just as you treat others with kindness.',
                    'author': 'SoulWhisper'
                },
                {
                    'content': 'Every morning is a new beginning, embrace the new day with hope.',
                    'author': 'SoulWhisper'
                },
                {
                    'content': 'Your heart is stronger than you think. Believe in yourself, you can do it.',
                    'author': 'SoulWhisper'
                },
                {
                    'content': 'Life is like a mirror. Smile at it, and it will smile back at you.',
                    'author': 'SoulWhisper'
                },
                {
                    'content': 'Every moment is the best arrangement. Cherish the present and live in the moment.',
                    'author': 'SoulWhisper'
                }
            ]

            # Initialize healing activities
            activities = [
                {
                    'title': 'Meditation Relaxation',
                    'description': 'Find a quiet place, close your eyes, breathe deeply, and let your thoughts calm down.',
                    'duration': 15,
                    'difficulty': 'easy'
                },
                {
                    'title': 'Gratitude Journal',
                    'description': 'Write down three things you are grateful for today, no matter how small.',
                    'duration': 10,
                    'difficulty': 'easy'
                },
                {
                    'title': 'Emotional Release',
                    'description': 'Release your emotions through exercise, painting, or writing.',
                    'duration': 30,
                    'difficulty': 'medium'
                },
                {
                    'title': 'Self-talk Letter',
                    'description': 'Write a letter to yourself, expressing care and support.',
                    'duration': 20,
                    'difficulty': 'medium'
                },
                {
                    'title': 'Mindful Walk',
                    'description': 'Take a walk outdoors, focus on the present moment, and observe your surroundings.',
                    'duration': 45,
                    'difficulty': 'easy'
                }
            ]

            # Create keywords
            for keyword_data in keywords:
                DailyKeyword.objects.get_or_create(
                    keyword=keyword_data['keyword'],
                    defaults={
                        'description': keyword_data['description'],
                        'is_active': True
                    }
                )

            # Create healing quotes
            for quote_data in quotes:
                HealingQuote.objects.get_or_create(
                    content=quote_data['content'],
                    defaults={
                        'author': quote_data['author'],
                        'is_active': True
                    }
                )

            # Create healing activities
            for activity_data in activities:
                HealingActivity.objects.get_or_create(
                    title=activity_data['title'],
                    defaults={
                        'description': activity_data['description'],
                        'duration': activity_data['duration'],
                        'difficulty': activity_data['difficulty'],
                        'is_active': True
                    }
                )

            self.stdout.write(self.style.SUCCESS('Successfully initialized daily content data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to initialize data: {str(e)}')) 