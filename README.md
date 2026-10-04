# 桌面语音智能体（Desktop AI Agent）

基于 LLM Function Calling 的本地桌面 AI 助手，支持语音唤醒、自然语言指令、软件操作、文件搜索、长期记忆与技术问答。

##  核心特性

-  **语音唤醒**：喊"诺诺"唤醒（Whisper 伪唤醒）
-  **语音识别**：本地 faster-whisper
-  **LLM 决策**：DeepSeek Function Calling
-  **17 个工具**：软件开关、文件搜索、网站打开、记忆管理、时间/天气/计算、系统监控
-  **长期记忆**：SQLite + ChromaDB（RAG 语义检索）
-  **知识库 RAG**：技术文档问答
- 🎵**自定义音色**：GPT-SoVITS 微调音色模型
-  **流式 TTS**：边合成边播放，低延迟

##  架构
desktop_agent/
├── core/ # Agent 决策层
│ ├── agent.py # LLM 调用 + 工具编排
│ ├── tools.py # 工具注册 + 分发
│ └── prompts.py # System Prompt
├── audio/ # 语音交互层
│ ├── asr.py # faster-whisper
│ ├── tts.py # GPT-SoVITS / edge-tts
│ └── wake.py # 唤醒词监听
├── memory/ # 记忆存储层
│ ├── store.py # SQLite
│ ├── vector_store.py # ChromaDB
│ └── knowledge_base.py # 知识库 RAG
├── apps/ # 系统操作层
│ ├── launcher.py # 软件扫描 + 启动
│ ├── app_control.py # 软件关闭 + 网站
│ ├── file_search.py # 文件搜索
│ ├── weather.py # 天气
│ ├── calculator.py # 计算
│ └── system_status.py # 系统监控
├── knowledge/ # 知识库文档
├── config.example.py # 配置示例（复制为 config.py 并填入 API Key）
└── main.py # 入口


## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt