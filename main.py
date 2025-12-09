import os
import tempfile
import time
import subprocess
import threading
import sounddevice as sd
import numpy as np
import requests
import pyautogui
from pynput import keyboard
from scipy.io.wavfile import write as write_wav
from dotenv import load_dotenv

load_dotenv()


API_URL = os.getenv("SILICONFLOW_API_URL", "https://api.siliconflow.cn/v1/audio/transcriptions")
API_TOKEN = os.getenv("SILICONFLOW_API_KEY")
MODEL = os.getenv("SILICONFLOW_MODEL", "FunAudioLLM/SenseVoiceSmall")
SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))

recording = False
audio_frames = []
stream = None
start_time = None
cmd_semicolon_pressed = False
pressed_keys = set()


def copy_to_clipboard(text):
    """复制文本到剪贴板 (macOS)"""
    process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    process.communicate(text.encode('utf-8'))


def paste_to_cursor(text, delay=0.5):
    """粘贴文本到当前光标位置"""
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.1

    copy_to_clipboard(text)
    time.sleep(0.1)

    if delay > 0:
        print(f"⏳ 准备粘贴...请切换到目标应用 ({delay:.1f}秒)")
        time.sleep(delay)

    try:
        print("📝 正在粘贴...")
        time.sleep(0.05)

        pyautogui.keyDown('command')
        time.sleep(0.01)
        pyautogui.keyDown('v')
        time.sleep(0.01)
        pyautogui.keyUp('v')
        pyautogui.keyUp('command')

        print("✅ 粘贴完成！")
    except Exception as e:
        print(f"❌ 粘贴失败: {e}")
        print("提示：请确保已授予 Python 屏幕录制/辅助功能权限")
    finally:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(b'')


def audio_callback(indata, frames, time_info, status):
    if recording:
        audio_frames.append(indata.copy())


def on_key_press(key):
    global cmd_semicolon_pressed, pressed_keys, paste_mode

    pressed_keys.add(key)

    try:
        if key == keyboard.KeyCode.from_char(';') and keyboard.Key.cmd in pressed_keys:
            if not cmd_semicolon_pressed and not recording:
                cmd_semicolon_pressed = True
                paste_mode = "clipboard"
                start_recording()
    except AttributeError:
        pass


def on_key_release(key):
    global cmd_semicolon_pressed, pressed_keys

    pressed_keys.discard(key)

    try:
        if key == keyboard.KeyCode.from_char(';'):
            if cmd_semicolon_pressed and recording:
                cmd_semicolon_pressed = False
                audio_path, record_time = stop_recording()

                if audio_path:
                    threading.Thread(target=process_audio, args=(audio_path, record_time), daemon=True).start()
    except AttributeError:
        pass


def process_audio(audio_path, record_time):
    text, inference_time = transcribe_audio(audio_path)
    os.unlink(audio_path)

    if text:
        copy_to_clipboard(text)
        print("📋 已复制到剪贴板!")
        paste_to_cursor(text, delay=0.5)
        print(f"⏱️  录音 {record_time:.2f}s | 转录 {inference_time:.2f}s | RTF {inference_time/record_time:.2f}x")


def start_recording():
    global recording, audio_frames, stream, start_time

    if recording:
        return

    audio_frames = []
    recording = True
    start_time = time.time()

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.int16,
        callback=audio_callback
    )

    stream.start()
    print("🎤 开始录音...")


def stop_recording():
    global recording, audio_frames, stream, start_time

    if not recording:
        return None, 0

    recording = False
    stream.stop()
    stream.close()

    record_time = time.time() - start_time

    if not audio_frames:
        print("没有录到音频")
        return None, 0

    audio_data = np.concatenate(audio_frames, axis=0)
    print(f"录音完成！时长 {record_time:.2f} 秒")

    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    write_wav(temp_file.name, SAMPLE_RATE, audio_data)
    return temp_file.name, record_time


def transcribe_audio(audio_path):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
    }

    print("📝 转录中...")
    start_time = time.time()
    with open(audio_path, "rb") as audio_file:
        files = {"file": audio_file}
        data = {"model": MODEL}
        response = requests.post(API_URL, headers=headers, files=files, data=data)

    inference_time = time.time() - start_time
    text = ""

    if response.status_code == 200:
        result = response.json()
        text = result.get("text", "")
        print(f"✅ 转录结果: {text}")
    else:
        print(f"❌ API 请求失败: {response.status_code}")
        print(response.text)

    return text, inference_time


def main():
    if not API_TOKEN:
        print("❌ 请在 .env 文件中设置 SILICONFLOW_API_KEY")
        return

    print("=" * 50)
    print("🎙️  语音转文字工具 v2.0")
    print()
    print("快捷键说明：")
    print("• Cmd + ; : 复制到剪贴板")
    print("• Option (Alt) + ; : 直接粘贴到光标位置")
    print()
    print("使用方法：")
    print("1. 按住相应快捷键开始录音")
    print("2. 松开按键自动停止并转录")
    print("3. 转录结果会根据模式自动处理")
    print()
    print("按 Ctrl+C 退出")
    print("=" * 50)
    print("\n程序已启动，等待按键触发...")
    print("提示：可能需要授予终端/Python辅助功能权限")
    print("      直接粘贴模式需要额外的屏幕录制/辅助功能权限")

    listener = keyboard.Listener(
        on_press=on_key_press,
        on_release=on_key_release
    )

    listener.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        if recording:
            stop_recording()
        print("\n👋 已退出")


if __name__ == "__main__":
    main()

