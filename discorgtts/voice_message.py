from pathlib import Path

from gtts import gTTS as speech
from tinytag import TinyTag


class VoiceMessage:
    def __init__(self):
        self.filepath = Path(__file__).parent / 'message.mp3'
        self.file = str(self.filepath)
        self.language = 'en-us'  # pull from config
        self.playing = False

    def generate_gtts(self, message):
        # may need a try except
        try:
            text_to_speech = speech(text=message,
                                    lang=self.language,
                                    slow=False)

            # maybe add sleep if a file exists
            if message:
                text_to_speech.save(self.file)
        except AssertionError as e:
            pass

    @property
    def file_exists(self):
        return self.filepath.exists()

    @property
    def mtime(self):
        if self.file_exists:
            return self.filepath.stat().st_mtime
        return None

    @property
    def duration(self):
        if self.file_exists:
            return round(TinyTag.get(self.file).duration) + 1
        return None

    def __len__(self):
        return self.duration

    def __repr__(self):
        text = f'filepath: {self.file}\n'\
            f'mtime: {self.mtime}\n'\
            f'duration: {self.duration}s'
        return text
