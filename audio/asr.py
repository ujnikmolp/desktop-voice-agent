"""语音识别模块（Whisper）"""
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
from config import WHISPER_MODEL, WHISPER_DEVICE, WHISPER_COMPUTE_TYPE, SAMPLE_RATE


# 加载模型（模块级，只加载一次）
_model = None


def get_model():
    global _model
    if _model is None:
        print("正在加载语音识别模型...")
        _model = WhisperModel(WHISPER_MODEL, device=WHISPER_DEVICE, compute_type=WHISPER_COMPUTE_TYPE)
        print("语音模型加载完成！")
    return _model


def record_audio(duration: int, sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    """录制指定时长的音频"""
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate,
                   channels=1, dtype="float32")
    sd.wait()
    return audio.flatten()


def speech_to_text(audio: np.ndarray) -> str:
    """把音频转成文字"""
    model = get_model()
    segments, _ = model.transcribe(audio, language="zh", beam_size=5)
    return "".join(seg.text for seg in segments).strip()