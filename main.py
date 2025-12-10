import os
import tempfile
import time
import subprocess
import threading
import sounddevice as sd
import numpy as np
from pynput import keyboard
from scipy.io.wavfile import write as write_wav
from dotenv import load_dotenv
from speech_transcription import create_transcription_manager

load_dotenv()

API_TOKEN = os.getenv("SILICONFLOW_API_KEY")
MODEL = os.getenv("SILICONFLOW_MODEL", "FunAudioLLM/SenseVoiceSmall")
SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))

# 创建语音转录管理器
transcription_manager = create_transcription_manager("siliconflow", api_key=API_TOKEN, model=MODEL)

recording = False
audio_frames = []
stream = None
start_time = None
cmd_semicolon_pressed = False
pressed_keys = set()


def initialize_paste_system():
    """初始化粘贴系统，确保资源就绪"""
    print("🔧 初始化粘贴系统...")
    
    # 预热剪贴板系统
    try:
        test_text = "warm_up_test"
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate(test_text.encode('utf-8'))
        
        # 验证剪贴板工作正常
        verify_process = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = verify_process.communicate()
        
        # 清理测试数据
        empty_process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        empty_process.communicate(b'')
        
        print("✅ 剪贴板系统就绪")
    except Exception as e:
        print(f"⚠️ 剪贴板预热警告: {e}")
    
    # 预热权限系统
    try:
        # 发送一个 AppleScript 命令来"唤醒"系统权限
        subprocess.run(['osascript', '-e', '''
        tell application "System Events"
            -- 触发权限检查但不实际执行操作
            get name of application process "System Events"
        end tell
        '''], capture_output=True, check=True)
        print("✅ 权限系统就绪")
    except Exception as e:
        print(f"⚠️ 权限预热警告: {e}")
    
    # 测试 AppleScript 功能
    try:
        test_applescript = '''
        tell application "System Events"
            -- 测试 AppleScript 基本功能
            delay 0.1
        end tell
        '''
        process = subprocess.run(['osascript', '-e', test_applescript], 
                               capture_output=True, text=True, timeout=3)
        if process.returncode == 0:
            print("✅ AppleScript 系统就绪")
        else:
            print(f"⚠️ AppleScript 预热失败: {process.stderr}")
    except Exception as e:
        print(f"⚠️ AppleScript 预热警告: {e}")
    
    time.sleep(0.2)  # 给系统一些时间完成初始化
    print("🚀 粘贴系统初始化完成")


def copy_to_clipboard(text):
    """复制文本到剪贴板 (macOS)"""
    try:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(text.encode('utf-8'))
        
        if process.returncode != 0:
            print(f"❌ 复制到剪贴板失败: {stderr.decode()}")
            return False
        return True
    except Exception as e:
        print(f"❌ 复制到剪贴板异常: {e}")
        return False


def verify_clipboard_content(expected_text):
    """验证剪贴板内容是否正确"""
    try:
        process = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            clipboard_content = stdout.decode('utf-8').strip()
            return expected_text.strip() in clipboard_content
    except Exception:
        pass
    return False


def paste_to_cursor(text, delay=0.1):
    """粘贴文本到当前光标位置 - 仅使用 AppleScript"""
    max_retries = 3
    
    # 确保文本已复制到剪贴板
    if not copy_to_clipboard(text):
        print("❌ 无法复制文本到剪贴板")
        return False
    
    if delay > 0:
        print(f"⏳ 准备粘贴... ({delay:.1f}秒)")
        time.sleep(delay)
    else:
        print("⚡ 立即粘贴...")
    
    for attempt in range(max_retries):
        try:
            print(f"📝 尝试粘贴 (第 {attempt + 1}/{max_retries} 次)...")
            
            # 确保剪贴板内容正确
            if not verify_clipboard_content(text):
                print("🔄 剪贴板内容验证失败，重新复制...")
                copy_to_clipboard(text)
                time.sleep(0.2)
            
            # 使用 AppleScript 粘贴
            try:
                print("🍎 执行 AppleScript 粘贴...")
                applescript = '''
                tell application "System Events"
                    -- 确保目标应用处于前台并获得焦点
                    delay 0.2
                    
                    -- 标准粘贴
                    try
                        keystroke "v" using command down
                        delay 0.1
                    on error
                        -- 如果失败，先激活应用再粘贴
                        activate
                        delay 0.1
                        keystroke "v" using command down
                    end try
                end tell
                '''
                
                process = subprocess.run(['osascript', '-e', applescript], 
                                       capture_output=True, text=True, timeout=8)
                
                if process.returncode == 0:
                    print("✅ 粘贴完成！")
                    time.sleep(0.3)  # 等待粘贴完成
                    return True
                else:
                    print(f"⚠️ 粘贴失败: {process.stderr}")
                    # 如果是权限错误，给出明确提示
                    if 'not allowed' in process.stderr.lower() or 'authorized' in process.stderr.lower():
                        print("🔑 检测到权限问题，请检查辅助功能权限")
                        
            except subprocess.TimeoutExpired:
                print("⚠️ 粘贴超时，请重试")
            except Exception as e1:
                print(f"⚠️ 粘贴异常: {e1}")
            
            if attempt < max_retries - 1:
                wait_time = 0.8 + (attempt * 0.3)  # 递增等待时间
                print(f"🔄 第 {attempt + 1} 次尝试失败，等待 {wait_time:.1f} 秒后重试...")
                time.sleep(wait_time)
                
        except Exception as e:
            print(f"❌ 第 {attempt + 1} 次粘贴尝试异常: {e}")
            if attempt < max_retries - 1:
                time.sleep(0.8)
    
    print("❌ 所有粘贴尝试均失败")
    print("🔧 故障排除建议：")
    print("   1. 检查系统偏好设置 → 安全性与隐私 → 屏幕录制权限")
    print("   2. 检查系统偏好设置 → 安全性与隐私 → 辅助功能权限")
    print("   3. 确保目标应用处于活动状态")
    print("   4. 尝试重启终端或重新运行程序")
    print("   5. 如果是首次运行，请在权限弹窗中点击'允许'")
    
    # 清理剪贴板（隐私保护）
    try:
        empty_clipboard = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        empty_clipboard.communicate(b'')
    except Exception:
        pass
    
    return False


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
    """处理音频文件 - 使用新的转录模块"""
    text, inference_time = transcription_manager.transcribe(audio_path)
    os.unlink(audio_path)

    if text:
        copy_to_clipboard(text)
        print("📋 已复制到剪贴板!")
        paste_to_cursor(text, delay=0)  # 无延迟，AppleScript 会自动处理应用切换
        print(f"⏱️  录音 {record_time:.2f}s | 转录 {inference_time:.2f}s | RTF {inference_time/record_time:.2f}x")
    else:
        print("❌ 转录失败或无内容")


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


def main():
    # 检查转录管理器配置
    if not transcription_manager.get_provider_info().get("configured", False):
        print("❌ 语音转录服务未配置")
        print("请在 .env 文件中设置 SILICONFLOW_API_KEY")
        return

    print("=" * 50)
    print("🎙️  语音转文字工具 v2.0")
    
    # 显示提供商信息
    provider_info = transcription_manager.get_provider_info()
    print(f"🔧 语音转录提供商: {provider_info['name']}")
    print(f"🤖 使用模型: {provider_info['model']}")
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
    print()

    # 初始化粘贴系统
    initialize_paste_system()

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

