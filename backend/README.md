# SoulWhisper Backend

SoulWhisper是一个情感日记应用的后端服务，提供用户管理、日记管理、语音转文字、情感分析等功能。

## 1. 项目结构

```
backend/
├── config/                 # 项目配置
│   ├── settings.py        # 项目设置（数据库、中间件等）
│   ├── urls.py            # 主URL路由配置
│   ├── wsgi.py            # WSGI应用配置
│   └── asgi.py           # ASGI应用配置
├── apps/                  # 应用模块
│   ├── account/          # 用户账户模块
│   │   ├── models.py     # 用户数据模型
│   │   ├── views.py      # 用户相关视图（登录、注册等）
│   │   └── urls.py       # 用户URL路由
│   ├── diary/            # 日记模块
│   │   ├── models.py     # 日记数据模型
│   │   ├── views.py      # 日记相关视图（含语音日记）
│   │   └── urls.py       # 日记URL路由
│   ├── chat/             # 聊天模块
│   │   ├── models.py     # 聊天数据模型
│   │   ├── views.py      # 聊天相关视图
│   │   └── urls.py       # 聊天URL路由
│   ├── community/        # 社区模块
│   │   ├── models.py     # 社区数据模型
│   │   ├── views.py      # 社区相关视图
│   │   └── urls.py       # 社区URL路由
│   └── utils/            # 工具模块
│       ├── asr/          # 语音识别工具
│       │   ├── asr_processor.py   # ASR处理核心
│       │   ├── whisper.py        # Whisper模型实现
│       │   └── onnx_asr.py      # ONNX优化版实现
│       └── middleware.py  # 中间件
├── ASR_model/            # ASR模型文件
│   ├── model/           # 原始模型
│   └── onnx/           # ONNX优化模型
├── temp_audio/          # 临时音频文件目录
├── logs/                # 日志文件目录
├── manage.py            # Django管理命令
└── requirements.txt     # 项目依赖

```

## 2. 模块说明

### Account模块
- 用户注册、登录功能
- 基于Token的用户认证
- 用户信息管理

### Diary模块
- 语音日记录制和转写
- 情感分析和标注
- 日记管理和查询

### Chat模块 (待实现)
- 与AI助手对话
- 情感倾诉和分析
- 会话历史管理

### Community模块 (待实现)
- 日记分享功能
- 评论和点赞
- 用户关注系统
- 内容审核机制

### Utils工具模块
- ASR语音识别服务
  - 支持多种音频格式
  - 集成Whisper模型
  - ONNX优化支持
- 情感分析服务
- 通用工具函数

## 3. 注意事项

### 数据库迁移
1. 修改数据库后需要进行迁移操作：
```bash
python manage.py makemigrations
python manage.py migrate
```

### API认证
1. 用户登录成功后会返回token
2. 后续所有需要认证的API请求都需要在Header中添加token：
```
Authorization: Token your_token_here
```

## 4. API接口说明

### 聊天接口

#### 开始日记对话
- **URL**: `/api/chat/start/`
- **方法**: POST
- **认证**: 需要Token认证
- **请求参数**:
  ```json
  {
    "diary_content": "用户的日记内容"
  }
  ```
- **响应**:
  ```json
  {
    "session_id": "会话ID",
    "response": "AI的首次回复"
  }
  ```

#### 发送聊天消息
- **URL**: `/api/chat/message/`
- **方法**: POST
- **认证**: 需要Token认证
- **请求参数**:
  ```json
  {
    "message": "用户的消息内容"
  }
  ```
- **响应**:
  ```json
  {
    "response": "AI的回复内容"
  }
  ```

#### 结束聊天会话
- **URL**: `/api/chat/end/`
- **方法**: POST
- **认证**: 需要Token认证
- **响应**:
  ```json
  {
    "message": "聊天会话已结束"
  }
  ```

### Community API

#### 获取每日内容
- **URL**: `/api/community/daily-content/`
- **方法**: GET
- **响应**:
  ```json
  {
    "date": "2024-01-01",
    "keyword": {
      "id": "keyword_id",
      "keyword": "Gratitude",
      "description": "Being thankful for what you have"
    },
    "quote": {
      "id": "quote_id",
      "content": "Life is not about where you are, but where you're going.",
      "author": "Holmes"
    },
    "activity": {
      "id": "activity_id",
      "title": "Mindful Meditation",
      "description": "Practice mindfulness through meditation",
      "duration": 15,
      "difficulty": "easy"
    }
  }
  ```

#### 获取评论列表
- **URL**: `/api/community/diaries/{diary_id}/comments/`
- **方法**: GET
- **响应**:
  ```json
  [
    {
      "id": "comment_id",
      "content": "Great writing!",
      "user_id": "user_id",
      "user_name": "username",
      "created_at": "2024-01-01 12:00:00",
      "updated_at": "2024-01-01 12:00:00"
    }
  ]
  ```

#### 创建评论
- **URL**: `/api/community/diaries/{diary_id}/comments/create/`
- **方法**: POST
- **请求体**:
  ```json
  {
    "content": "Great writing!"
  }
  ```
- **响应**:
  ```json
  {
    "id": "comment_id",
    "content": "Great writing!",
    "user_id": "user_id",
    "user_name": "username",
    "created_at": "2024-01-01 12:00:00",
    "updated_at": "2024-01-01 12:00:00"
  }
  ```

#### 更新评论
- **URL**: `/api/community/comments/{comment_id}/update/`
- **方法**: PUT
- **请求体**:
  ```json
  {
    "content": "Updated comment"
  }
  ```
- **响应**:
  ```json
  {
    "id": "comment_id",
    "content": "Updated comment",
    "user_id": "user_id",
    "user_name": "username",
    "created_at": "2024-01-01 12:00:00",
    "updated_at": "2024-01-01 12:00:00"
  }
  ```

#### 删除评论
- **URL**: `/api/community/comments/{comment_id}/delete/`
- **方法**: DELETE
- **响应**: 204 No Content

### Diary API

#### 语音识别创建日记
- **URL**: `/api/diary/asr/`
- **方法**: POST
- **请求体**: FormData
  - audio_file: 音频文件 (支持 .wav, .mp3, .m4a, .flac)
- **响应**:
  ```json
  {
    "text": "转写的文本内容",
    "emotion_type": "happy",
    "emotion_intensity": 8,
    "diary_id": "diary_id"
  }
  ```

#### 获取日记列表
- **URL**: `/api/diary/diaries/`
- **方法**: GET
- **响应**:
  ```json
  {
    "count": 10,
    "next": "next_page_url",
    "previous": "previous_page_url",
    "results": [
      {
        "id": "diary_id",
        "content": "日记内容",
        "emotion_type": "happy",
        "emotion_intensity": 8,
        "created_at": "2024-01-01 12:00:00",
        "comment_count": 5
      }
    ]
  }
  ```

#### 创建日记
- **URL**: `/api/diary/diaries/create/`
- **方法**: POST
- **请求体**:
  ```json
  {
    "content": "日记内容",
    "emotion_type": "happy",
    "emotion_intensity": 8
  }
  ```
- **响应**:
  ```json
  {
    "id": "diary_id",
    "content": "日记内容",
    "emotion_type": "happy",
    "emotion_intensity": 8,
    "created_at": "2024-01-01 12:00:00"
  }
  ```

#### 获取日记详情
- **URL**: `/api/diary/diaries/{diary_id}/`
- **方法**: GET
- **响应**:
  ```json
  {
    "id": "diary_id",
    "content": "日记内容",
    "emotion_type": "happy",
    "emotion_intensity": 8,
    "created_at": "2024-01-01 12:00:00"
  }
  ```

#### 更新日记
- **URL**: `/api/diary/diaries/{diary_id}/update/`
- **方法**: PUT
- **请求体**:
  ```json
  {
    "content": "更新的日记内容",
    "emotion_type": "happy",
    "emotion_intensity": 8
  }
  ```
- **响应**:
  ```json
  {
    "id": "diary_id",
    "content": "更新的日记内容",
    "emotion_type": "happy",
    "emotion_intensity": 8,
    "created_at": "2024-01-01 12:00:00"
  }
  ```

#### 删除日记
- **URL**: `/api/diary/diaries/{diary_id}/delete/`
- **方法**: DELETE
- **响应**: 204 No Content


