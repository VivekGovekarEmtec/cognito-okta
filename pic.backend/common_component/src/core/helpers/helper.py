from enum import Enum
import re
import json


class CaseInsensitiveEnum(str, Enum):
    @classmethod
    def _missing_(cls, value: str):
        for member in cls:
            if member.lower() == value.lower():
                return member
        return None


class SortDirections(CaseInsensitiveEnum):
    asc = 'asc'
    desc = 'desc'
    ASC = ''


def remove_keys(data, keys):
    return [{k: v for k, v in d.items() if k != keys} for d in data]


def title_case(input_str):
    return re.sub(
        r"[A-Za-z]+('[A-Za-z]+)?",
        lambda word: word.group(0).capitalize(),
        input_str)


def get_query_param_value(event, parameter, totype):
    try:
        value = event.get(parameter, None)
        if value is not None:
            return totype(value)
        return value
    except ValueError as e:
        raise e


def response_headers():
    headers = {
        "access-control-allow-origin": '*',
        "Strict-Transport-Security": "Strict-Transport-Security: max-age=31536000; includeSubDomains",
        "X-Frame-Options": "SAMEORIGIN",
        "X-Content-Type-Options": "nosniff"
    }
    return headers


def create_response(response):
    result = {
        'statusCode': response["status_code"],
        'body': json.dumps(response),
        "headers": response_headers()
    }
    return result
