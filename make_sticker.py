import tinify
import uuid
import os
import datetime
import random

global keys
keys = ["dqqaz9991qKoBM16lQs6jFxNzLeTTv0J", "uom7RdRYoAd7BZVy8MGq5UnktvSIMnJT", "Lt6yTb4jYZz36tZkazs7wDHh_31Gs3So"]


def convert(url):
    tinify.key = keys[0]
    try:
        source = tinify.from_url(url)
    except AccountError:
        keys.pop(0)
        return convert(url)
    resized = source.resize(method="fit", width=512, height=512)
    name = str(uuid.uuid4())[:12] + ".png"
    today = datetime.date.today().strftime("%Y%m%d")
    todaypath = "convert_stickers/" + str(today)
    os.makedirs(todaypath, exist_ok=True)
    path = todaypath+ "/" + name
    resized.to_file(path)
    return path
