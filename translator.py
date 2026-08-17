from deep_translator import GoogleTranslator

def ua_to_ru(text):
    return GoogleTranslator(source='uk', target='ru').translate(text)