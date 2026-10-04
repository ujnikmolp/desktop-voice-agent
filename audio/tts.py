"""语音合成模块：调用 GPT-SoVITS API（流式）"""
import os
import time
import uuid
import tempfile
import requests
import numpy as np
import sounddevice as sd
from config import (
    GPT_SOVITS_API, GPT_SOVITS_REF_AUDIO, GPT_SOVITS_PROMPT_TEXT,
    STREAMING_MODE, SAMPLE_RATE_TTS
)


STATE = {"enabled": True}


def speak(text: str):
    """流式 TTS：边合成边播放"""
    if not STATE["enabled"] or not text.strip():
        return

    max_retries = 2
    for attempt in range(max_retries):
        try:
            payload = {
                "text": text,
                "text_lang": "zh",
                "ref_audio_path": GPT_SOVITS_REF_AUDIO,
                "prompt_text": GPT_SOVITS_PROMPT_TEXT,
                "prompt_lang": "zh",
                "text_split_method": "cut0",
                "media_type": "wav",
                "streaming_mode": STREAMING_MODE,
            }

            # 流式请求
            with requests.post(
                GPT_SOVITS_API, json=payload, stream=True, timeout=120
            ) as r:
                if r.status_code != 200:
                    raise Exception(f"API 返回 {r.status_code}")

                # 打开音频输出流
                with sd.OutputStream(
                    samplerate=SAMPLE_RATE_TTS,
                    channels=1,
                    dtype="int16"
                ) as stream:
                    # 边收边播
                    for chunk in r.iter_content(chunk_size=4096):
                        if not chunk:
                            continue
                        audio_np = np.frombuffer(chunk, dtype=np.int16)
                        stream.write(audio_np)

            return  # 成功就退出

        except Exception as e:
            if attempt < max_retries - 1:
                print(f"[语音重试 {attempt + 1}/{max_retries}]")
                time.sleep(1)
            else:
                print(f"[语音暂不可用] {e}")


def mute():
    STATE["enabled"] = False


def unmute():
    STATE["enabled"] = True


def is_enabled() -> bool:
    return STATE["enabled"]