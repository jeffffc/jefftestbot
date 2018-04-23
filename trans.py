from yandex_translate import YandexTranslate
from config import *

translate = YandexTranslate(YANDEX_API)


def trans(text):
    inputlang = translate.detect(text)
    output = translate.translate(text, 'en')
    outputtext = output['text'][0]
    return inputlang, outputtext


def trans2(to_langcode, text):
    inputlang = translate.detect(text)
    outputlang = to_langcode
    convert = inputlang + "-" + outputlang
    output = translate.translate(text, convert)
    outputtext = output['text'][0]
    return inputlang, outputtext
