from deep_translator import GoogleTranslator

from tools.logging import logger

translator_en = GoogleTranslator(source="auto", target="en")
translator_ru = GoogleTranslator(source="auto", target="ru")


def translate_to_english(text: str) -> str:
    try:
        translated_text = translator_en.translate(text.encode("utf-8", "replace").decode("utf-8"))
    except Exception as e:
        logger.error(f"Error in translation: {e}")
        translated_text = text
    return translated_text


def translate_to_russian(text: str) -> str:
    try:
        translated_text = translator_ru.translate(text.encode("utf-8", "replace").decode("utf-8"))
    except Exception as e:
        logger.error(f"Error in translation: {e}")
        translated_text = text
    return translated_text
