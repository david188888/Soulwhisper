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

#### 2. Database Setup (MongoDB+uniCloud)

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

**uniCloud Cloud Database Setup (for production)**
- uniCloud is a cloud service integrated with DCloud's ecosystem, using MongoDB-compatible databases. Here's how to configure it:

- Steps:
1. **Install HBuilderX (the official IDE for uniApp).**
2. **Register and authenticate a DCloud account.**
3. **Create a Cloud Service Space:**
- Open HBuilderX → Go to uniCloud → Click New Cloud Service Space.
- Choose Alibaba Cloud Free Tier (recommended for starters) and follow the prompts to create.
4. **Associate Database with Cloud Space:**
- In HBuilderX, right-click the database folder in your project → Select Initialize Database.
5. **Upload Cloud Functions & Modules:**
- Right-click the cloudfunction folder → Select Upload All Cloud Functions, Public Modules, and Actions.
- This deploys your backend logic to the uniCloud server.

- Note: uniCloud databases are managed via HBuilderX and the DCloud console, with built-in features like authentication, serverless functions, and monitoring. For more details, refer to [the uniCloud Official Documentation](https://doc.dcloud.net.cn/uniCloud/).

#### 3. Start Services

**Backend:**
```bash
cd backend
# Apply migrations and migrate database
python manage.py makemigrations
python manage.py migrate

# start the Django development server
python manage.py runserver
```

**Frontend:**
Click the "Preview" button in the top right corner of HBuilderX to directly debug your frontend page in HBuilder's built-in browser. If the window size is limited, you can choose to zoom in the browser for debugging.

### API Configuration

**Note**: API keys are already pre-configured and ready to use. If the current API keys don't work or you want to use your own, you can configure them in `backend/config/settings.py`.

#### API Services & Models Used:

1. **XUNFEI (iFlytek) Speech Recognition**
   - **Official Website**: [IFlytek](https://www.xfyun.cn/)
   - **Documentation**: [API document](https://www.xfyun.cn/doc/asr/ifasr_new/API.html)
   - **Configuration**: `XUNFEI_APPID` & `XUNFEI_API_SECRET`
   - **Purpose**: Speech-to-text conversion for voice diary

2. **Alibaba Cloud DashScope (Qwen Audio)**
   - **Official Website**: [Aliyun model website ](https://bailian.console.aliyun.com/?spm=5176.29597918.J_tAwMEW-mKC1CPxlfy227s.1.f3a57b08nMo0jk&tab=model#/model-market)
   - **Documentation**: [API document](https://bailian.console.aliyun.com/?spm=5176.29597918.J_tAwMEW-mKC1CPxlfy227s.1.f3a57b08nMo0jk&tab=api#/api/?type=model&url=https%3A%2F%2Fhelp.aliyun.com%2Fdocument_detail%2F2845960.html)
   - **Model Used**: `qwen-audio-turbo-latest`
   - **Configuration**: `AUDIO_TURBO_API_KEY`
   - **Purpose**: Audio emotion analysis

3. **ZHIPU AI (ChatGLM)**
   - **Official Website**: [ZHIPU AI](https://open.bigmodel.cn/)
   - **Documentation**: [API document](https://open.bigmodel.cn/dev/api)
   - **Model Used**: `glm-4-air`
   - **Configuration**: `ZHIPUAI_API_KEY`
   - **Purpose**: LLM conversational chatbot for emotional companionship

#### If Current API Keys Don't Work:
If you encounter issues with the pre-configured API keys, you have the following options:

1. **Contact for Support**: Feel free to reach out to the repository owner or contributors for assistance with the API keys. Email: david.liu1888888@gmail.com
2. **Configure Your Own Keys**: 
   - Visit the official websites above
   - Sign up for developer accounts
   - Follow their documentation to obtain API keys
   - Replace the keys in `backend/config/settings.py`
3. **Follow Official Tutorials**: Each platform provides comprehensive setup guides and documentation


### Important Notes
1. Ensure MongoDB service is running before starting the backend
2. API keys are already configured and ready to use
