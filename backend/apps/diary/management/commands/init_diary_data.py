from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.diary.models import Diary
from apps.account.models import User

class Command(BaseCommand):
    help = '初始化日记数据到MongoDB'

    def handle(self, *args, **kwargs):
        try:
            # 确保有一个测试用户
            try:
                user = User.objects.get(username='testuser')
                self.stdout.write(self.style.SUCCESS(f'找到已存在的用户: {user.username}'))
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username='testuser',
                    password='testpassword',
                    name='测试用户',
                    sex='M'
                )
                self.stdout.write(self.style.SUCCESS(f'创建新用户: {user.username}'))

            # 示例日记内容
            diary_contents = [
                {
                    'content': '今天心情特别好，和朋友一起去公园散步，阳光明媚，感觉整个人都充满活力。看到小朋友们在玩耍，心情格外愉悦。',
                    'emotion': 'happy',
                    'intensity': 8
                },
                {
                    'content': '工作压力有点大，项目deadline快到了，感觉有些焦虑。需要调整一下心态，好好规划时间。',
                    'emotion': 'neutral',
                    'intensity': 6
                },
                {
                    'content': '今天很平静，按部就班地完成了工作，午休时看了会书，感觉生活节奏刚刚好。',
                    'emotion': 'neutral',
                    'intensity': 5
                },
                {
                    'content': '和家人视频，听说奶奶身体不太好，心里有些难过。希望她能早日康复。',
                    'emotion': 'sad',
                    'intensity': 7
                },
                {
                    'content': '收到了期待已久的offer！太开心了！这段时间的努力终于有了回报，感觉整个人都在发光！',
                    'emotion': 'happy',
                    'intensity': 9
                },
                {
                    'content': '连续加班三天了，感觉身心俱疲。需要好好休息一下，调整状态。',
                    'emotion': 'neutral',
                    'intensity': 7
                },
                {
                    'content': '地铁上遇到很不礼貌的人，故意加塞还瞪人，真是气死我了。深呼吸，不要跟这种人一般见识。',
                    'emotion': 'angry',
                    'intensity': 6
                }
            ]

            # 清除已有的测试数据
            Diary.objects.filter(user=user).delete()
            self.stdout.write(self.style.SUCCESS('清除已有数据'))

            # 插入新的日记数据
            for i, content_data in enumerate(diary_contents):
                date = timezone.now() - timedelta(days=i)
                diary = Diary.objects.create(
                    user=user,
                    content=content_data['content'],
                    emotion_type=content_data['emotion'],
                    emotion_intensity=content_data['intensity'],
                    created_at=date
                )
                self.stdout.write(self.style.SUCCESS(f'插入第 {i+1} 条日记'))

            self.stdout.write(self.style.SUCCESS(f'成功为用户 {user.username} 创建示例日记数据'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'初始化数据失败: {str(e)}')) 