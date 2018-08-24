from pathlib import Path
from multiprocessing import Queue

from gtts import gTTS as speech
from tinytag import TinyTag
from time import sleep

from filelock import FileLock


class VoiceMessageFile:
    def __init__(self):
        self.filepath = Path(__file__).parent / 'message.mp3'
        self.file = str(self.filepath)
        self.filelock = FileLock(self.filepath.with_suffix('.lock'), timeout=0.01)
        # self.language = 'en-au'  # en-au, en-us, en-uk, random

    def create_message(self, message, language):
        print('creating message')
        msg = speech(text=message,
                     lang=language,
                     slow=False)
        print('saving message')
        msg.save(self.file)
        print('done writing file')

    @property
    def duration(self):
        '''returns the duration of the audio file in seconds'''
        if self.file_exists:
            return round(TinyTag.get(self.file).duration) + 1
        return None

    @property
    def mtime(self):
        '''returns the most recent content modification expressed in seconds'''
        if self.file_exists:
            return self.filepath.stat().st_mtime
        return None

    @property
    def file_exists(self):
        '''returns True if file exists'''
        return self.filepath.exists()

    def remove(self):
        if self.file_exists:
            # sleep(.5)
            self.filepath.unlink()

    def __len__(self):
        return self.duration

    def __repr__(self):
        text = f'filepath: {self.file}\n'\
            f'mtime: {self.mtime}\n'\
            f'duration: {self.duration}s'
        return text


class VoiceMessageQueue:
    '''Stores messages waiting to be processed in a FIFO queue.'''
    _message_queue = Queue()
    # XXX: test out lifo, and lifo with a max

    def push(message):
        '''Pushes new message to queue.'''
        VoiceMessageQueue._message_queue.put(message)

    def pop():
        '''retuns True if the queue is empty.'''
        return VoiceMessageQueue._message_queue.get()

    def is_empty():
        return VoiceMessageQueue._message_queue.empty()
