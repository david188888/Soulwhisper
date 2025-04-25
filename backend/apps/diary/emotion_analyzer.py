from django.db.models import Count
from datetime import datetime, timedelta
from .models import Diary
from django.db.models.functions import TruncDate
from collections import defaultdict
import jieba
import jieba.analyse
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

class EmotionAnalyzer:
    def __init__(self, user):
        self.user = user
        # 情绪映射表
        self.emotions = {
            'happy': '开心',
            'sad': '悲伤',
            'angry': '愤怒',
            'calm': '平静',
            'anxious': '焦虑',
            'excited': '兴奋',
            'tired': '疲惫'
        }
        # 情绪对应的颜色
        self.emotion_colors = {
            'happy': '#FF6B6B',    # 红色
            'sad': '#4ECDC4',      # 青色
            'angry': '#FF4949',    # 深红
            'calm': '#45B7D1',     # 蓝色
            'anxious': '#FFBE0B',  # 黄色
            'excited': '#96CEB4',  # 绿色
            'tired': '#D4A5A5'     # 粉色
        }
        # MongoDB连接
        self.client = pymongo.MongoClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_NAME]
        self.diary_collection = self.db['diary']

    def get_recent_diaries(self, days=7):
        """获取用户最近n天的日记"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 从MongoDB获取数据
        diaries = self.diary_collection.find({
            'user_id': str(self.user.id),
            'created_at': {
                '$gte': start_date,
                '$lte': end_date
            }
        }).sort('created_at', -1)
        
        return list(diaries)

    def generate_word_cloud(self):
        """生成词云图"""
        diaries = self.get_recent_diaries()
        if not diaries:
            return None, ["快记录心情，看看你都在想什么吧"]
            
        # 合并所有日记内容
        text = ' '.join(diary['content'] for diary in diaries)
        
        # 使用jieba进行分词和关键词提取
        keywords = jieba.analyse.extract_tags(text, topK=20, withWeight=True)
        
        # 创建词云对象
        wc = WordCloud(
            font_path="C:/Windows/Fonts/simhei.ttf",  # Windows系统中文字体路径
            width=400,
            height=200,
            background_color='white',
            max_words=100,
            colormap='Set2'  # 使用matplotlib的Set2配色方案
        )
        
        # 生成词云
        word_freq = {word: weight for word, weight in keywords}
        wc.generate_from_frequencies(word_freq)
        
        # 将词云图转换为base64字符串
        img = io.BytesIO()
        wc.to_image().save(img, format='PNG')
        img_str = base64.b64encode(img.getvalue()).decode()
        
        # 返回词云图base64字符串和关键词列表
        return img_str, [word for word, _ in keywords[:10]]

    def analyze_emotions(self):
        """分析情绪分布"""
        diaries = self.get_recent_diaries()
        if not diaries:
            return {
                'emotions': defaultdict(int),
                'keywords': []
            }
        
        # 统计情绪分布
        emotion_counts = defaultdict(int)
        for diary in diaries:
            emotion = diary.get('emotion', 'neutral')
            emotion_counts[emotion] += 1
            
        # 生成词云和关键词
        _, keywords = self.generate_word_cloud()
        
        # 计算情绪百分比
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
        """生成情绪分布饼图"""
        emotion_data = self.analyze_emotions()
        emotions = emotion_data['emotions']
        
        if not emotions:
            return None
            
        # 设置中文显示
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 创建饼图
        plt.figure(figsize=(8, 8))
        labels = list(emotions.keys())
        sizes = list(emotions.values())
        colors = [self.emotion_colors.get(k, '#9B9B9B') for k in emotions.keys()]
        
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
        plt.axis('equal')
        
        # 将图表转换为base64字符串
        img = io.BytesIO()
        plt.savefig(img, format='PNG', bbox_inches='tight', dpi=100)
        plt.close()
        img_str = base64.b64encode(img.getvalue()).decode()
        
        return img_str 