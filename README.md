# SoulWhisper

An AI-powered emotional companion and anonymous healing platform focused on young people's mental health needs. Provides private emotional outlets and spiritual healing services through intelligent voice diary, emotional data analysis, anonymous community, and AI psychological companionship.

## Features

- **Intelligent Voice Diary**: Voice recording, automatic speech-to-text, emotion analysis
- **Emotional Data Visualization**: Quantify emotional states, generate emotion reports
- **Anonymous Community**: Emotional drift bottles, secure emotional communication platform
- **AI Psychological Companion**: LLM conversational chatbot for conversational companionship, instant emotional support

## Tech Stack

**Backend**: Django + MongoDB + AI Model Integration(api)  
**Frontend**: uni-app + Vue3 (supports H5/Mini-programs/App)

## Quick Start

### Requirements

**Backend**:  
- Python 3.11.9
- MongoDB 8.0.5

**Frontend**:  
- HBuilderX or Node.js 14+
- uni-app development environment

### Installation & Deployment

#### 1. Clone Repository & Install Dependencies

```bash
# Clone the repository
git clone git@github.com:david188888/Soulwhisper.git
cd SoulWhisper

# Install all dependencies in root directory
pip install -r requirements.txt
```

#### 2. Database Setup (MongoDB)

**Download & Install MongoDB:**
- Download MongoDB Community Server from: https://www.mongodb.com/try/download/community
- Install MongoDB following the official installation guide for your operating system

**Start MongoDB:**(We recommend using MongoDB Compass to manage your database visually)
```bash
# Windows (if installed as service)
net start MongoDB

# Linux/Mac
sudo systemctl start mongod
# or
mongod --dbpath /data/db
```

**Configuration:**
- Default connection: `mongodb://localhost:27017`
- Database name: `soulwhisper` (automatically created)

#### 3. Start Services

**Backend:**
```bash
cd backend
python manage.py runserver
```

**Frontend:**
```bash
# Option 1: Using HBuilderX
# 1. Open HBuilderX, import project
# 2. Run -> Run to Browser -> Chrome

# Option 2: Using command line
npm install
npm run dev:h5
```

### API Configuration

**Note**: API keys are already pre-configured and ready to use. If the current API keys don't work or you want to use your own, you can configure them in `backend/config/settings.py`.

#### API Services & Models Used:

1. **XUNFEI (iFlytek) Speech Recognition**
   - **Official Website**: https://www.xfyun.cn/
   - **Developer Console**: https://console.xfyun.cn/
   - **Documentation**: https://www.xfyun.cn/doc/asr/voicedictation/API.html
   - **Configuration**: `XUNFEI_APPID` & `XUNFEI_API_SECRET`
   - **Purpose**: Speech-to-text conversion for voice diary

2. **Alibaba Cloud DashScope (Qwen Audio)**
   - **Official Website**: https://dashscope.aliyun.com/
   - **Documentation**: https://help.aliyun.com/zh/dashscope/
   - **Model Used**: `qwen-audio-turbo-latest`
   - **Configuration**: `AUDIO_TURBO_API_KEY`
   - **Purpose**: Audio emotion analysis and processing

3. **ZHIPU AI (ChatGLM)**
   - **Official Website**: https://open.bigmodel.cn/
   - **Documentation**: https://open.bigmodel.cn/dev/api
   - **Model Used**: `glm-4-air`
   - **Configuration**: `ZHIPUAI_API_KEY`
   - **Purpose**: AI conversational companion and psychological support

#### If Current API Keys Don't Work:

If you encounter issues with the pre-configured API keys, you have the following options:

1. **Contact for Support**: Feel free to reach out for assistance with API configuration
2. **Configure Your Own Keys**: 
   - Visit the official websites above
   - Sign up for developer accounts
   - Follow their documentation to obtain API keys
   - Replace the keys in `backend/config/settings.py`
3. **Follow Official Tutorials**: Each platform provides comprehensive setup guides and documentation


### Important Notes

1. Ensure MongoDB service is running before starting the backend
2. API keys are already configured and ready to use
3. Audio features need HTTPS or localhost environment
4. Recommended to test full functionality in Chrome browser