import ctypes
import threading
winmm = ctypes.windll.winmm


def PlayMidi(file_path):
    # 打开MIDI文件
    winmm.mciSendStringW(f'open "{file_path}" alias midi', None, 0, 0)
    stop_event = threading.Event()
    def play_thread():
        winmm.mciSendStringW('play midi', None, 0, 0)
        while not stop_event.is_set():
            status = ctypes.create_unicode_buffer(32)
            winmm.mciSendStringW('status midi mode', status, 32, 0)
            if status.value != 'playing':
                break
            threading.Event().wait(0.1)
        winmm.mciSendStringW('close midi', None, 0, 0)
    thread = threading.Thread(target=play_thread)
    thread.start()
    return stop_event

PlayMidi("./InspirationSong.mid")