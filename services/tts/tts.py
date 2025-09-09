from faster_whisper import WhisperModel
import io
import logging
from services.utils.utils import Logger


class Tts:
    def __init__(self, model_size: str = "base"):
        self.__model = WhisperModel(model_size, device="cpu", compute_type="int8")
        self.__logger = Logger.get_logger("TTS")

    def transcribe(self, audio_bytes: bytes, language: str = None, vad_filter: bool = True) -> str:
        try:
            segments, info = self.__model.transcribe(io.BytesIO(audio_bytes), language= language, vad_filter=vad_filter)
            full_text = " ".join([segment.text for segment in segments])
            self.__logger.info(f"Successfully transcribe audio")
            return full_text
        except Exception as e:
            self.__logger.error(f"Failed to transcribe audio: {e}")
            raise e
    
  