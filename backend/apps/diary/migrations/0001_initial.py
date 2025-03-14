# Generated by Django 4.2.20 on 2025-03-14 04:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Diary",
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
                (
                    "title",
                    models.CharField(blank=True, max_length=200, verbose_name="标题"),
                ),
                ("content", models.TextField(verbose_name="内容")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "is_public",
                    models.BooleanField(default=False, verbose_name="是否公开"),
                ),
                (
                    "dominant_emotion",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="主要情感"
                    ),
                ),
                (
                    "emotion_data",
                    models.JSONField(blank=True, null=True, verbose_name="情感数据"),
                ),
                (
                    "audio_file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="diary_audio/",
                        verbose_name="音频文件",
                    ),
                ),
            ],
            options={
                "verbose_name": "日记",
                "verbose_name_plural": "日记",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="DiaryTag",
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
                ("name", models.CharField(max_length=50, verbose_name="标签名")),
                (
                    "description",
                    models.CharField(blank=True, max_length=200, verbose_name="描述"),
                ),
            ],
            options={
                "verbose_name": "日记标签",
                "verbose_name_plural": "日记标签",
            },
        ),
        migrations.CreateModel(
            name="DiaryTagging",
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
                (
                    "diary",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="diary.diary",
                        verbose_name="日记",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="diary.diarytag",
                        verbose_name="标签",
                    ),
                ),
            ],
            options={
                "verbose_name": "日记标签关联",
                "verbose_name_plural": "日记标签关联",
                "unique_together": {("diary", "tag")},
            },
        ),
        migrations.AddField(
            model_name="diary",
            name="tags",
            field=models.ManyToManyField(
                related_name="diaries",
                through="diary.DiaryTagging",
                to="diary.diarytag",
                verbose_name="标签",
            ),
        ),
        migrations.AddField(
            model_name="diary",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="diaries",
                to=settings.AUTH_USER_MODEL,
                verbose_name="用户",
            ),
        ),
    ]
