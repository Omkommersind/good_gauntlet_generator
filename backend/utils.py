import csv
import json
import random
import string
import time
from collections import OrderedDict
from typing import List

import requests
import urllib.error
import urllib.parse

from datetime import datetime, timedelta
from functools import reduce

from django.core.mail import EmailMessage

import pytz
from django.template.loader import get_template
from django.utils.safestring import SafeString
from django.utils.timezone import make_aware
from rest_framework import status

from backend.exceptions import InternalServerException
from fabula_server.settings import EMAIL_HOST_USER


def choices(em):
    return [(e.value, e.name) for e in em]


def datetime_to_milliseconds(dt: datetime):
    try:
        # для возможности выбора дат за пределами границ таймштампа используем разницу дат с эпохой
        # replace(tzinfo=None) используется для удаления информации о временной зоне, чтобы получить разность
        diff = dt.replace(tzinfo=None) - datetime(1970, 1, 1)
        large_timestamp = int(diff.total_seconds() * 1000)
        return large_timestamp
    except Exception as e:
        print(e)
        return None


def milliseconds_to_datetime(milliseconds, tz: str = None):
    """ Перевод из любого таймштампа в дату """
    # make_aware используется для учета временной зоны (учитывается в БД)
    overflowed_date = make_aware(datetime(1970, 1, 1) + timedelta(milliseconds=milliseconds))
    if tz is not None:
        tz = pytz.timezone(tz)
        return overflowed_date.replace(tzinfo=tz)
    return overflowed_date


def date_to_milliseconds(date):
    return datetime_to_milliseconds(datetime.combine(date, datetime.min.time()))


def timedelta_to_milliseconds(td: timedelta):
    return int(td.total_seconds() * 1000)


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def chained_get(obj, *args, default=None):
    def get_value(o, attr):
        if isinstance(o, dict) and isinstance(attr, str):
            return o.get(attr, default)
        if isinstance(o, (list, tuple)) and isinstance(attr, int):
            return o[attr]
        if isinstance(o, object) and isinstance(attr, str):
            return getattr(o, attr, default)
        return None

    try:
        result = reduce(get_value, args, obj)
        return result
    except Exception:
        return default


def utc_now_with_tz():
    utc_now = datetime.utcnow()
    return datetime.combine(utc_now.date(), utc_now.time(), tzinfo=pytz.utc)


def send_email(subject: str, message: str, from_email: str, to_email: []):
    try:
        email = EmailMessage(subject, message, from_email=from_email, to=to_email)
        return email.send()
    except Exception as ex:
        raise InternalServerException(str(ex))


def send_formatted_email(subject: str, template_name: str, context: dict, to_email: list):
    from django.core.mail import get_connection

    connection = get_connection()
    try:
        message = get_template(template_name).render(context)

        msg = EmailMessage(subject, message, from_email=f'Fabula <{EMAIL_HOST_USER}>', to=to_email)
        msg.content_subtype = "html"
        msg.send()
    except Exception as ex:
        raise InternalServerException(str(ex))


def exponential_backoff_request(url: str, method: str, headers: dict = None, data: dict = None, params: dict = None):
    if headers is None:
        headers = {}
    if params is None:
        params = {}
    if data is None:
        data = {}
    else:
        data = json.dumps(data)

    print('Executing external api request to ' + url)

    current_delay = 0.1  # Set the initial retry delay to 100ms.
    max_delay = 5  # Set the maximum retry delay to 5 seconds.

    while True:
        try:
            # Get the API response.
            response = requests.request(method, url, headers=headers, data=data, params=params)

            # if response.status_code != 200:
            #     print('Error external api request:')
            #     print('Text: ', response.text)
            #     print('URL: ' + url)
            #     raise InternalServerException(json.loads(response.text))
        except urllib.error.URLError:
            pass  # Fall through to the retry loop.
        else:
            # If we didn't get an IOError then parse the result.
            return response

        if current_delay > max_delay:
            raise InternalServerException('External service not responded')

        time.sleep(current_delay)
        current_delay *= 2  # Increase the delay each time we retry.


def get_response_data(response):
    if response.status_code == status.HTTP_200_OK or response.status_code == status.HTTP_204_NO_CONTENT:
        try:
            return response.json(), response.status_code
        except:
            return '', response.status_code
    else:
        raise InternalServerException(
            f'Distant service exception: detail={json.loads(response.text)}, status_code={response.status_code}')


def safe_string_for_template(s: str) -> str:
    return SafeString(s.replace('\\', '\\\\').replace('\'', '\\\''))


def remove_fields_from_dict_with_lists_recursively(d: dict, fields_to_remove: List[str]) -> dict:
    for key in list(d):
        if key in fields_to_remove:
            del d[key]
        elif isinstance(d[key], list):
            processed_list = []
            for obj in d[key]:
                if isinstance(obj, dict) or isinstance(obj, OrderedDict):
                    processed_list.append(remove_fields_from_dict_with_lists_recursively(obj, fields_to_remove))
                else:
                    processed_list.append(obj)
            d[key] = processed_list
        elif isinstance(d[key], dict) or isinstance(d[key], OrderedDict):
            d[key] = remove_fields_from_dict_with_lists_recursively(d[key], fields_to_remove)
    return d


def save_list_to_csv(path: str, data: []):
    with open(path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for row in data:
            writer.writerow(row)


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
