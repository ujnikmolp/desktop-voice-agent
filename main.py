"""程序入口"""
import sys
from memory.store import init_db, list_memory
from audio.asr import get_model
from audio.tts import speak, mute, unmute
from audio.wake import wait_for_wake_word, record_command
from core.agent import chat
from apps.launcher import APP_PATHS
from memory.knowledge_base import build_knowledge_base


def run_wake_mode():
    """待机模式：喊唤醒词后交互"""
    print(f"\n👂 已进入待机模式，说「诺诺」唤醒我")
    print("（按 Ctrl+C 退出程序）\n")

    while True:
        try:
            # 等待唤醒
            wait_for_wake_word()
            speak("我在")

            # 录音识别指令
            cmd = record_command()
            if not cmd:
                print("没听清，回到待机")
                continue

            print(f"你：{cmd}")
            reply = chat(cmd)
            print(f"诺诺：{reply}")
            speak(reply)

            print(f"\n👂 回到待机模式")

        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"[运行出错] {e}")


def run_cli_mode():
    """命令行模式"""
    print("\n命令说明：")
    print("  直接输入文字 → 文字模式")
    print("  输入 voice   → 语音模式（录音5秒）")
    print("  输入 list    → 查看所有可用软件")
    print("  输入 mem     → 查看所有记忆")
    print("  输入 mute    → 关闭语音回复")
    print("  输入 unmute  → 开启语音回复")
    print("  输入 exit    → 退出")

    from audio.asr import record_audio, speech_to_text

    while True:
        user_input = input("\n你：").strip()

        if user_input.lower() == "exit":
            break
        if user_input.lower() == "list":
            print(f"共 {len(APP_PATHS)} 个软件：")
            for name in sorted(APP_PATHS.keys()):
                print(f"  - {name}")
            continue
        if user_input.lower() == "mem":
            print(list_memory())
            continue
        if user_input.lower() == "mute":
            mute()
            print("已静音")
            continue
        if user_input.lower() == "unmute":
            unmute()
            print("已开启语音回复")
            continue

        if user_input.lower() == "voice":
            print("🎤 正在录音 5 秒...请说话")
            audio = record_audio(5)
            user_input = speech_to_text(audio)
            if not user_input:
                print("没有听清楚，请再试一次")
                continue
            print(f"识别结果：{user_input}")

        if not user_input:
            continue

        reply = chat(user_input)
        print(f"诺诺：{reply}")
        speak(reply)


def main():
    # 初始化
    init_db()
    build_knowledge_base()
    get_model()

        # 预热 TTS（不发声）
    print("正在预热语音合成...")
    import requests
    from config import (
        GPT_SOVITS_API, GPT_SOVITS_REF_AUDIO,
        GPT_SOVITS_PROMPT_TEXT, STREAMING_MODE
    )
    try:
        payload = {
            "text": "预热",
            "text_lang": "zh",
            "ref_audio_path": GPT_SOVITS_REF_AUDIO,
            "prompt_text": GPT_SOVITS_PROMPT_TEXT,
            "prompt_lang": "zh",
            "text_split_method": "cut0",
            "media_type": "wav",
            "streaming_mode": STREAMING_MODE,
        }
        requests.post(GPT_SOVITS_API, json=payload, stream=True, timeout=60)
        print("预热完成")
    except Exception as e:
        print(f"预热失败（不影响使用）：{e}")

    print(f"\n已扫描到 {len(APP_PATHS)} 个软件")
    print("\n请选择模式：")
    print("  1 → 待机模式（喊「诺诺」唤醒，推荐）")
    print("  2 → 文字/语音命令行模式")
    choice = input("输入 1 或 2：").strip()

    if choice == "1":
        run_wake_mode()
    else:
        run_cli_mode()


if __name__ == "__main__":
    main()