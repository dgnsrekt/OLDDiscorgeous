from pathlib import Path
from multiprocessing import Queue

from gtts import gTTS as speech
from tinytag import TinyTag
from time import sleep


class VoiceMessageFile:
    def __init__(self):
        self.filepath = Path(__file__).parent / 'message.mp3'
        self.file = str(self.filepath)
        self.language = 'en-au'  # en-au, en-us, en-uk, random

    @property
    def language_setting():
        pass

    def create_message(self, message):
        msg = speech(text=message,
                     lang=self.language,
                     slow=False)
        msg.save(self.file)

    @property
    def duration(self):
        if self.file_exists:
            return round(TinyTag.get(self.file).duration) + 1
        return None

    @property
    def mtime(self):
        if self.file_exists:
            return self.filepath.stat().st_mtime
        return None

    @property
    def file_exists(self):
        return self.filepath.exists()

    def delete(self):
        if self.file_exists:
            sleep(1)
            self.filepath.unlink()

    def __len__(self):
        return self.duration

    def __repr__(self):
        text = f'filepath: {self.file}\n'\
            f'mtime: {self.mtime}\n'\
            f'duration: {self.duration}s'
        return text


class VoiceMessageQueue:
    _message_queue = Queue()
    # XXX: test out lifo, and lifo with a max

    def push(message):
        VoiceMessageQueue._message_queue.put(message)

    def pop():
        return VoiceMessageQueue._message_queue.get()

    def is_empty():
        return VoiceMessageQueue._message_queue.empty()


x = VoiceMessageFile()
print(x.mtime)
print(x.duration)
print(x)
