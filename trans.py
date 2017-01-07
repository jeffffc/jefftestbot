from yandex_translate import YandexTranslate
from config import *

translate = YandexTranslate(YANDEX_API)

def trans(text):
    inputlang = translate.detect(text)
    output = translate.translate(text, 'en')
    outputtext = output['text'][0]
    return inputlang, outputtext

