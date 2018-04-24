from google.cloud import translate

gtranslate = translate.Client.from_service_account_json("translate_cred.json", target_language='en')


def trans(text, lang=None):
    if lang:
        output = gtranslate.translate(text, target_language=lang)
    else:
        output = gtranslate.translate(text)
    outputtext = output['translatedText']
    source_lang = output['detectedSourceLanguage']
    return source_lang, outputtext
