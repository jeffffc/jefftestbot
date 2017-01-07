#!/bin/bash
#import sys
#import os
#import subprocess
#import goslate
#from translate import translator
#from googletrans import translator
from yandex_translate import YandexTranslate

translate = YandexTranslate('trnsl.1.1.20170105T150217Z.672e65c941ac42b8.0ddaa2677d1d56a71c4f9833191efe39e4b02f63')
#gs = goslate.Goslate()

def trans(text):
#    return translator('en', text)
#    cmd = "trans :en %s" % text
#    cmd = subprocess.call(["translate", ":en", text])
#    test = cmd
#    print(test)
#    output = translator.translate(text)
#    return output
    inputlang = translate.detect(text)
    output = translate.translate(text, 'en')
    outputtext = output['text'][0]
    return inputlang, outputtext

#trans("你好, 做緊咩呀")
