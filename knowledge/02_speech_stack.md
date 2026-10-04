# 语音交互链路：ASR + TTS

## ASR 是什么
ASR（Automatic Speech Recognition）是把语音转成文字。我的项目用 faster-whisper。

## 为什么用 faster-whisper
1. 本地部署：不需要联网，隐私好
2. 免费：不需要付费 API
3. 中文识别准确率高：small 模型约 92%
4. 对比 OpenAI Whisper API：不需要上传音频、不需要付费

## faster-whisper 的使用
模型大小：tiny、base、small、medium、large。我用 small，在准确率和速度之间平衡。
加载时指定 device="cpu"、compute_type="int8" 降低资源占用。

## TTS 是什么
TTS（Text-to-Speech）是把文字转成语音。我的项目用 edge-tts。

## 为什么用 edge-tts
1. 免费：微软 Edge 浏览器的语音合成引擎
2. 音质自然：接近真人
3. 多音色：晓晓、云希、云扬等多种中文音色
4. 对比 Azure TTS：不需要注册、不需要 Key

## 完整语音交互链路
唤醒词检测 → ASR 识别 → LLM 决策 → 工具执行 → TTS 合成 → 播放

## 语音合成容错
edge-tts 偶发 503（微软服务器限流）。处理：重试 3 次，每次间隔 1.5 秒；
3 次都失败就静默降级，不中断主流程。