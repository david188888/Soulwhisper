# SoulWhisper Backend

SoulWhisper是一个情感日记应用的后端服务，提供用户管理、日记管理、语音转文字、情感分析等功能。

## 项目结构

```
backend/
├── config/                 # 项目配置
│   ├── settings.py         # 项目设置（数据库、中间件等）
│   ├── urls.py             # 主URL路由配置
│   └── wsgi.py             # WSGI应用配置
├── soul_backend/           # 主应用包
│   ├── account/            # 用户账户模块
│   │   ├── models.py       # 用户数据模型
│   │   ├── views.py        # 用户相关视图
│   │   └── urls.py         # 用户URL路由
│   ├── diary/              # 日记模块
│   │   ├── models.py       # 日记数据模型
│   │   ├── views.py        # 日记相关视图（含语音日记）
│   │   └── urls.py         # 日记URL路由
│   ├── chat/               # 聊天模块
│   │   ├── models.py       # 聊天数据模型
│   │   ├── views.py        # 聊天相关视图
│   │   └── urls.py         # 聊天URL路由
│   ├── community/          # 社区模块
│   │   ├── models.py       # 社区数据模型（评论、点赞等）
│   │   ├── views.py        # 社区相关视图
│   │   └── urls.py         # 社区URL路由
│   ├── utils/              # 工具模块
│   │   ├── asr/            # 语音识别工具
│   │   │   └── whisper_asr.py  # ASR核心实现
│   │   └── emotion/        # 情感分析工具
│   │       └── emotion_analysis.py  # 情感分析实现
│   └── admin.py            # 统一的管理界面配置
├── ASR_model/              # ASR模型文件
│   └── model/              # 预训练模型和配置
├── temp_audio/            # 临时音频文件目录（自动创建和清理）
├── logs/                  # 日志文件
├── manage.py             # Django命令行工具
└── requirements.txt      # 项目依赖列表
```

## 模块说明

### 1. Account模块
- 用户注册、登录、登出
- 用户资料管理
- 用户认证和授权

### 2. Diary模块
- 文本日记管理
- 语音日记（自动转写）
- 情感分析标注
- 日记列表和详情

### 3. Chat模块
- 聊天会话管理
- 消息收发
- 历史记录查询

### 4. Community模块
- 评论管理
- 点赞功能
- 用户关注
- 社区互动

### 5. Utils工具模块
- ASR语音识别
- 情感分析服务
- 通用工具函数

## 模块间调用

### 1. 模型调用

```python
# 在其他模块中导入模型
from apps.diary.models import Diary
from apps.account.models import User

# 使用示例
diary = Diary.objects.create(
    user=user,
    title="标题",
    content="内容"
)
```

### 2. 工具函数调用

```python
# 在视图中使用工具函数
from apps.utils import transcribe_audio, analyze_emotion

# 使用示例
text = transcribe_audio(audio_file)
emotion = analyze_emotion(text)
```

### 3. URL配置
主URL配置（config/urls.py）统一管理所有模块的路由：
```python
urlpatterns = [
    path('api/account/', include('apps.account.urls')),
    path('api/diary/', include('apps.diary.urls')),
    path('api/chat/', include('apps.chat.urls')),
    path('api/community/', include('apps.community.urls')),
]
```

## Admin统一管理

项目使用统一的管理界面配置（soul_backend/admin.py），主要特点：

1. **自定义用户管理**
```python
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'mood')
    search_fields = ('username', 'email')
```

2. **日记管理**
```python
@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'dominant_emotion')
    list_filter = ('dominant_emotion', 'created_at')
```

3. **聊天记录管理**
```python
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'sender', 'created_at')
    list_filter = ('created_at',)
```

访问管理界面：
1. 创建超级用户：`python manage.py createsuperuser`
2. 访问：`http://localhost:8000/admin/`

## 环境配置

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. requirements.txt 主要依赖
```
Django==5.0.2
djangorestframework==3.14.0
torch==2.2.0
transformers==4.37.2
python-dotenv==1.0.1
psycopg2-binary==2.9.9  # PostgreSQL数据库驱动
```

### 3. 环境变量配置
创建 `.env` 文件：
```env
DEBUG=True
SECRET_KEY=your_secret_key
```

### 4. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

## 开发指南

1. **创建新的应用模块**
```bash
python manage.py startapp new_module
```

2. **添加新数据库模型**
- 在 `models.py` 中定义数据库模型
- 在 `admin.py` 中注册数据库模型
- 执行数据库迁移

3. **添加新的API端点**
- 在 `views.py` 中创建视图
- 在模块的 `urls.py` 中添加URL配置
- 在主 `urls.py` 中包含新模块的URLs

## 注意事项

1. **ASR模型文件**
- 确保 `ASR_model/model/` 目录包含所有必要的模型文件
- 首次使用时会自动下载预训练模型

2. **临时音频文件处理**
- 语音文件临时存储在 `temp_audio/` 目录
- 文件处理完成后自动清理
- 目录不存在时会自动创建
- 使用UUID生成唯一文件名，避免冲突

3. **日志**
- 日志文件存储在 `logs/` 目录
- 可在 `settings.py` 中配置日志级别
