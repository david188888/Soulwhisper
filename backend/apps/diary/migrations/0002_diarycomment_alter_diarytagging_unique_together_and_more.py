# Generated by Django 4.2.20 on 2025-03-14 07:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("diary", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiaryComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField(verbose_name="评论内容")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="评论时间"),
                ),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="是否删除"),
                ),
                (
                    "like_count",
                    models.PositiveIntegerField(default=0, verbose_name="点赞数"),
                ),
            ],
            options={
                "verbose_name": "日记评论",
                "verbose_name_plural": "日记评论",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AlterUniqueTogether(
            name="diarytagging",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="diarytagging",
            name="diary",
        ),
        migrations.RemoveField(
            model_name="diarytagging",
            name="tag",
        ),
        migrations.RemoveField(
            model_name="diary",
            name="audio_file",
        ),
        migrations.RemoveField(
            model_name="diary",
            name="dominant_emotion",
        ),
        migrations.RemoveField(
            model_name="diary",
            name="emotion_data",
        ),
        migrations.AddField(
            model_name="diary",
            name="allow_comments",
            field=models.BooleanField(default=True, verbose_name="允许评论"),
        ),
        migrations.AddField(
            model_name="diary",
            name="category",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="分类"
            ),
        ),
        migrations.AddField(
            model_name="diary",
            name="comment_count",
            field=models.PositiveIntegerField(default=0, verbose_name="评论数"),
        ),
        migrations.AddField(
            model_name="diary",
            name="images",
            field=models.TextField(
                blank=True,
                help_text="多个图片链接请用逗号分隔",
                null=True,
                verbose_name="图片链接",
            ),
        ),
        migrations.AddField(
            model_name="diary",
            name="latitude",
            field=models.DecimalField(
                blank=True,
                decimal_places=6,
                max_digits=9,
                null=True,
                verbose_name="纬度",
            ),
        ),
        migrations.AddField(
            model_name="diary",
            name="like_count",
            field=models.PositiveIntegerField(default=0, verbose_name="点赞数"),
        ),
        migrations.AddField(
            model_name="diary",
            name="location",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="位置"
            ),
        ),
        migrations.AddField(
            model_name="diary",
            name="longitude",
            field=models.DecimalField(
                blank=True,
                decimal_places=6,
                max_digits=9,
                null=True,
                verbose_name="经度",
            ),
        ),
        migrations.AddField(
            model_name="diary",
            name="mood",
            field=models.CharField(
                choices=[
                    ("happy", "开心"),
                    ("sad", "难过"),
                    ("angry", "生气"),
                    ("excited", "兴奋"),
                    ("calm", "平静"),
                    ("worried", "担忧"),
                    ("tired", "疲惫"),
                    ("lonely", "孤独"),
                    ("grateful", "感恩"),
                    ("confused", "困惑"),
                    ("hopeful", "希望"),
                    ("loved", "被爱"),
                ],
                default="calm",
                max_length=10,
                verbose_name="心情",
            ),
        ),
        migrations.AddField(
            model_name="diary",
            name="view_count",
            field=models.PositiveIntegerField(default=0, verbose_name="查看次数"),
        ),
        migrations.AddField(
            model_name="diary",
            name="weather",
            field=models.CharField(
                choices=[
                    ("sunny", "晴天"),
                    ("cloudy", "多云"),
                    ("rainy", "下雨"),
                    ("snowy", "下雪"),
                    ("windy", "刮风"),
                    ("foggy", "雾天"),
                    ("thunderstorm", "雷暴"),
                    ("overcast", "阴天"),
                    ("hazy", "霾"),
                    ("hot", "炎热"),
                    ("cold", "寒冷"),
                ],
                default="sunny",
                max_length=15,
                verbose_name="天气",
            ),
        ),
        migrations.RemoveField(
            model_name="diary",
            name="tags",
        ),
        migrations.AlterField(
            model_name="diary",
            name="title",
            field=models.CharField(max_length=100, verbose_name="标题"),
        ),
        migrations.AddIndex(
            model_name="diary",
            index=models.Index(
                fields=["-created_at"], name="diary_diary_created_d3d854_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="diary",
            index=models.Index(
                fields=["user", "-created_at"], name="diary_diary_user_id_8cafd2_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="diary",
            index=models.Index(
                fields=["is_public", "-created_at"],
                name="diary_diary_is_publ_e2eaa7_idx",
            ),
        ),
        migrations.DeleteModel(
            name="DiaryTag",
        ),
        migrations.DeleteModel(
            name="DiaryTagging",
        ),
        migrations.AddField(
            model_name="diarycomment",
            name="diary",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="diary_comments",
                to="diary.diary",
                verbose_name="日记",
            ),
        ),
        migrations.AddField(
            model_name="diarycomment",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                to="diary.diarycomment",
                verbose_name="父评论",
            ),
        ),
        migrations.AddField(
            model_name="diarycomment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="diary_comments",
                to=settings.AUTH_USER_MODEL,
                verbose_name="评论用户",
            ),
        ),
        migrations.AddField(
            model_name="diary",
            name="tags",
            field=models.CharField(
                blank=True,
                help_text="多个标签请用逗号分隔",
                max_length=200,
                null=True,
                verbose_name="标签",
            ),
        ),
    ]
