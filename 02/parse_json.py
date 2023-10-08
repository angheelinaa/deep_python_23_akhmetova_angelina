import json


def parse_json(json_str: str, required_fields=None, keywords=None, keyword_callback=None):
    if required_fields is None or keywords is None:
        raise TypeError("required_fields and keywords should be a list of str")

    if keyword_callback is None:
        raise TypeError("missing required keyword_callback function")

    json_doc = json.loads(json_str)
    for field in required_fields:
        if field in json_doc:
            words_list = json_doc[field].lower().split()
            for key_word in keywords:
                if key_word.lower() in words_list:
                    keyword_callback(key_word, field)


def keyword_callback_function(*args):
    pass
