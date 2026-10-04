# 桌面语音智能体（Desktop AI Agent）

基于 LLM Function Calling 的本地桌面 AI 助手，支持语音唤醒、自然语言指令、软件操作、文件搜索、长期记忆与技术问答。

## ✨ 核心特性

- 🎙️ **语音唤醒**：喊"诺诺"唤醒（Whisper 伪唤醒）
- 🗣️ **语音识别**：本地 faster-whisper
- 🧠 **LLM 决策**：DeepSeek Function Calling
- 🔧 **15 个工具**：软件开关、文件搜索、网站打开、记忆管理、时间/天气/计算、系统监控
- 💾 **长期记忆**：SQLite + ChromaDB（RAG 语义检索）
- 📚 **知识库 RAG**：技术文档问答
- 🎵 **自定义音色**：GPT-SoVITS 微调音色模型
- ⚡ **流式 TTS**：边合成边播放，低延迟

## 🏗️ 架构
