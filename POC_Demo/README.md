# SoulWhisper POC Demo

## 概述
本项目为 SoulWhisper 情感日记应用的概念验证(POC)演示。主要目的是展示后端核心AI功能模块，并验证其可行性。

本POC遵循项目提交要求：
- **核心功能**：专注于关键算法和组件，证明概念可行性
- **简单界面**：命令行界面，便于功能演示
- **数据处理**：从固定数据文件读取输入，无需数据库
- **最小化实现**：优先功能实现而非性能优化

## 核心功能演示
本POC支持**双模式运行**，既可调用真实API，也可使用模拟数据演示：

### 🔗 真实API模式 (推荐用于完整演示)
- **语音识别**: 讯飞长语音识别API
- **情感分析**: 通义语音大模型API + 智谱AI GLM-4-Air
- **AI对话**: 智谱AI GLM-4-Air
- 需要有效的API密钥配置

### 🔧 模拟演示模式 (推荐用于功能验证)  
- **语音识别**: 基于文件名的模拟识别
- **情感分析**: 关键词匹配算法
- **AI对话**: 规则模板回复系统
- 无需API密钥，可直接体验功能流程

### 主要功能模块
1. **语音识别 (ASR)**: 将音频样本转换为文字
   - 对应后端模块: `backend/apps/utils/asr/asr_processor.py`
2. **情感分析**: 分析文本情感倾向和强度  
   - 对应后端模块: `backend/apps/utils/llm/get_result.py`
3. **AI对话伙伴**: 基于情感状态的智能对话
   - 对应后端模块: `backend/apps/utils/llm/get_result.py`

## 目录结构
```
POC_Demo/
├── README.md                 # 项目说明文件
├── config.py                 # 配置文件
├── requirements_simple.txt   # 核心依赖包列表
├── requirements.txt          # 完整依赖包列表
├── main_demo_simple.py       # 主演示程序
├── start_demo.bat           # Windows启动脚本
├── API_INTERFACE_GUIDE.md   # API接口隔离说明文档
├── core/                     # 核心演示逻辑
│   ├── __init__.py           # 模块初始化文件
│   ├── asr_demo.py           # 语音识别演示接口 (支持双模式)
│   ├── emotion_demo.py       # 情感分析演示接口 (支持双模式)
│   ├── chat_demo.py          # AI对话演示接口 (支持双模式)
│   └── utils.py              # 辅助工具函数
├── audio_samples/            # 存放测试用音频文件
│   ├── happy_sample.wav      # 快乐情感音频样本
│   ├── sad_sample.mp3        # 悲伤情感音频样本
│   ├── neutral_sample.wav    # 中性情感音频样本
│   └── README.md             # 音频样本说明
├── data/                     # 存放测试用的文本数据
│   └── text_samples.json     # 文本样本数据
└── output/                   # 存放演示结果
    └── (运行时生成的分析结果文件)
```

## 安装与运行

### 系统要求
- Python 3.7 或更高版本
- Windows 操作系统（推荐）

### 快速启动 (推荐)
1. **双击运行 `start_demo.bat`**
   - 脚本会自动检查Python环境
   - 自动安装必要依赖
   - 启动演示程序

### 手动安装与运行
1. **安装依赖**:
   ```powershell
   # 安装核心依赖（推荐）
   pip install -r requirements_simple.txt
   
   # 或安装完整依赖
   pip install -r requirements.txt
   ```

2. **运行演示**:
   ```powershell
   python main_demo_simple.py
   ```

### 功能演示
程序启动后，可选择以下功能进行演示：
1. **语音识别 (ASR)**: 选择音频文件进行语音转文字
2. **情感分析**: 输入文本进行情感分析
3. **AI对话**: 基于情感状态进行智能对话
4. **完整流程**: 演示从语音识别→情感分析→AI对话的完整工作流程

### 模式切换配置
在 `config.py` 中可以控制运行模式：

```python
# 设置为 True 使用真实API (需要API密钥配置)
# 设置为 False 使用模拟演示模式 (无需API密钥)
USE_REAL_BACKEND = False  # 默认使用模拟模式
```

**真实API模式特点:**
- ✅ 展示实际的AI能力
- ⚠️ 需要有效的API密钥
- 🌐 需要网络连接
- 💰 可能产生API调用费用

**模拟演示模式特点:**
- ✅ 快速体验功能流程  
- ✅ 无需API密钥
- ✅ 离线运行
- ✅ 完全免费

### 输出结果说明
系统会标明数据来源以便区分：
- `"source": "real_backend"` - 真实API结果
- `"source": "mock_data"` - 模拟数据结果
- `"source": "real_backend_fallback"` - API故障时的降级结果

## 项目架构

### 与后端项目的关系
此POC Demo是后端功能的演示界面，不包含独立的数据存储或复杂的用户管理。所有核心AI处理可以连接后端项目或使用内置模拟数据。

### 运行模式
**模拟模式** (默认，USE_REAL_BACKEND=False):
- 使用内置模拟数据和逻辑
- 无需配置后端环境
- 适合快速演示和测试

**真实后端模式** (USE_REAL_BACKEND=True):
- 连接并调用后端模块进行处理
- 需要配置后端环境
- 展示真实功能效果

## 配置说明

### 核心配置 (config.py)
- `USE_REAL_BACKEND`: 设置为 `True` 连接真实后端，`False` 使用模拟数据
- `BACKEND_PROJECT_ROOT`: 后端项目路径 (相对于POC_Demo目录)
- `DATA_DIR`: 测试数据目录
- `AUDIO_DIR`: 音频样本目录
- `OUTPUT_DIR`: 输出结果目录

## 提交规范符合性

本POC严格按照项目提交要求设计：

### 1. PoC软件 (20%权重)
✅ **核心功能**: 实现语音识别、情感分析、AI对话的关键算法和组件  
✅ **最小化实现**: 提供证明概念可行性的最小实现  
✅ **简单界面**: 命令行界面，专注于功能演示  
✅ **数据处理**: 从固定文件读取输入，无需数据库集成  

### 2. 提交包内容
✅ **源代码**: 所有Python源文件  
✅ **启动脚本**: start_demo.bat可执行脚本  
✅ **用户手册**: README.md项目文档  

### 3. 评估标准
✅ **核心功能**: 令人信服地演示关键思想的可行性  
✅ **文档质量**: 清晰、完整的安装和使用说明  
✅ **规范遵循**: 严格遵守提交指南和格式要求  

## 注意事项

- 本POC主要用于功能演示和概念验证
- 音频文件支持格式：.wav, .mp3
- 确保 `audio_samples/` 目录下有测试音频文件
- 所有分析结果会自动保存到 `output/` 目录
- 如需修改核心AI功能，请在 `backend` 项目中进行
- 如遇到依赖问题，请检查Python版本是否为3.7+
