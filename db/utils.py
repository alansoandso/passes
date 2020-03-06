from pretty_json import format_json


def pprint(json):
    print(pformat(json), flush=True)


def pformat(json):
    return format_json(json, 'solarized')
