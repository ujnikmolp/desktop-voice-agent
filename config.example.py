"""全局配置示例

使用说明：
1. 复制本文件为 config.py
2. 填入你自己的 DeepSeek API Key
"""
import os
from pathlib import Path

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# ============ LLM 配置 ============
API_KEY = "your-deepseek-api-key-here"   # ← 换成你的
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"

# ============ 语音配置 ============
VOICE = "zh-CN-XiaoxiaoNeural"
WHISPER_MODEL = "small"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"

# ============ 唤醒词配置 ============
WAKE_WORD = "诺诺"
WAKE_LISTEN_DURATION = 1.2
COMMAND_DURATION = 5
VOLUME_THRESHOLD = 0.001

# ============ 音频配置 ============
SAMPLE_RATE = 16000

# ============ 路径配置 ============
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "data" / "memory.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# ============ GPT-SoVITS 配置 ============
GPT_SOVITS_API = "http://127.0.0.1:9880/tts"
GPT_SOVITS_REF_AUDIO = r"D:/GPT-SoVITS/ref.wav"
GPT_SOVITS_PROMPT_TEXT = "孤立夜色的古堡终于显出真实的模样"

# ============ 流式 TTS 配置 ============
STREAMING_MODE = 2
SAMPLE_RATE_TTS = 32000