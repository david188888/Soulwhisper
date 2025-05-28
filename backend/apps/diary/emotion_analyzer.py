from django.db.models import Count
from datetime import datetime, timedelta
from .models import Diary
from django.db.models.functions import TruncDate
from collections import defaultdict
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image
import numpy as np
import os
import pymongo
from django.conf import settings
from bson import ObjectId
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class EmotionAnalyzer:
    def __init__(self, user):
        self.user = user
        # Emotion mapping table
        self.emotions = {
            'happy': 'Happy',
            'sad': 'Sad',
            'angry': 'Angry',
            'calm': 'Calm',
            'anxious': 'Anxious',
            'excited': 'Excited',
            'tired': 'Tired'
        }
        # Colors for each emotion
        self.emotion_colors = {
            'happy': '#FF6B6B',    # Red
            'sad': '#4ECDC4',      # Cyan
            'angry': '#FF4949',    # Deep red
            'calm': '#45B7D1',     # Blue
            'anxious': '#FFBE0B',  # Yellow
            'excited': '#96CEB4',  # Green
            'tired': '#D4A5A5'     # Pink
        }
        # MongoDB connection
        self.client = pymongo.MongoClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_NAME]
        self.diary_collection = self.db['diary']

    def get_recent_diaries(self, days=7):
        """Get user's diaries from the last n days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get data from MongoDB
        diaries = self.diary_collection.find({
            'user_id': str(self.user.id),
            'created_at': {
                '$gte': start_date,
                '$lte': end_date
            }
        }).sort('created_at', -1)
        
        return list(diaries)

    def generate_word_cloud(self):
        """Generate word cloud"""
        diaries = self.get_recent_diaries()
        if not diaries:
            return None, ["Start recording your thoughts to see what's on your mind"]
            
        # Combine all diary content
        text = ' '.join(diary['content'] for diary in diaries)
        
        # Use NLTK for word tokenization
        words = word_tokenize(text.lower())
        
        # Filter stop words and short words
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word.isalnum() and word not in stop_words and len(word) > 2]
        
        # Count word frequency
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Create word cloud object
        wc = WordCloud(
            width=400,
            height=200,
            background_color='white',
            max_words=100,
            colormap='Set2'  # Use matplotlib's Set2 color scheme
        )
        
        # Generate word cloud
        wc.generate_from_frequencies(word_freq)
        
        # Convert word cloud to base64 string
        img = io.BytesIO()
        wc.to_image().save(img, format='PNG')
        img_str = base64.b64encode(img.getvalue()).decode()
        
        # Return word cloud base64 string and keyword list
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        return img_str, [word for word, _ in top_words]

    def analyze_emotions(self):
        """Analyze emotion distribution"""
        diaries = self.get_recent_diaries()
        if not diaries:
            return {
                'emotions': defaultdict(int),
                'keywords': []
            }
        
        # Count emotion distribution
        emotion_counts = defaultdict(int)
        for diary in diaries:
            emotion = diary.get('emotion', 'neutral')
            emotion_counts[emotion] += 1
            
        # Generate word cloud and keywords
        _, keywords = self.generate_word_cloud()
        
        # Calculate emotion percentages
        total = sum(emotion_counts.values())
        emotion_percentages = {
            self.emotions.get(k, k): round((v / total) * 100, 1)
            for k, v in emotion_counts.items()
        }
        
        return {
            'emotions': emotion_percentages,
            'keywords': keywords
        }

    def generate_emotion_chart(self):
        """Generate emotion distribution pie chart"""
        emotion_data = self.analyze_emotions()
        emotions = emotion_data['emotions']
        
        if not emotions:
            return None
            
        # Create pie chart
        plt.figure(figsize=(8, 8))
        labels = list(emotions.keys())
        sizes = list(emotions.values())
        colors = [self.emotion_colors.get(k, '#9B9B9B') for k in emotions.keys()]
        
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
        plt.axis('equal')
        
        # Convert chart to base64 string
        img = io.BytesIO()
        plt.savefig(img, format='PNG', bbox_inches='tight', dpi=100)
        plt.close()
        img_str = base64.b64encode(img.getvalue()).decode()
        
        return img_str