"""唤醒词监听模块"""
import time
import numpy as np
from config import WAKE_WORD, WAKE_LISTEN_DURATION, COMMAND_DURATION, VOLUME_THRESHOLD
from audio.asr import record_audio, speech_to_text


# 调试开关
DEBUG = False


def wait_for_wake_word() -> str:
    """
    阻塞等待唤醒词。
    返回识别到的指令文本（已经过验证），失败返回 None。
    """
    while True:
        try:
            # 录一小段
            audio = record_audio(WAKE_LISTEN_DURATION)

            # 音量门控，太安静直接跳过
            volume = np.abs(audio).mean()
            if volume < VOLUME_THRESHOLD:
                continue

            # 识别
            text = speech_to_text(audio)
            if not text:
                continue

            if DEBUG:
                print(f"[监听中] {text}")

            # 检测唤醒词（多关键词模糊匹配）
            WAKE_KEYWORDS = [
                "诺诺", "糯糯", "喏喏", "诺若", "洛洛", "娜娜",
                "懦懦", "诺诺子", "诺洛","諾諾" ,"诺","nono",
            ]
            if any(kw in text for kw in WAKE_KEYWORDS):
                print(f"✅ 唤醒！（听到：{text}）")
                return text

        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"[监听出错] {e}")
            time.sleep(1)


def record_command() -> str:
    """唤醒后，录制用户指令"""
    print(f"🎤 请说指令（{COMMAND_DURATION}秒）...")
    audio = record_audio(COMMAND_DURATION)
    return speech_to_text(audio)