import urllib3
import json

from termcolor import colored

from config import ADDR, CONFIG


def get_questions(lesson_name, dest_addr=ADDR) -> list:
    http_headers_w10_get = {
        'Host': f'{dest_addr}',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43',
        'Referer': f'http://{dest_addr}/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7'
    }
    return http_request(http_fields={'lessonName': lesson_name}, http_headers=http_headers_w10_get,
                        url=f'http://{dest_addr}', path='/questions/get')


def send_answers(http_payload, dest_addr=ADDR) -> dict:
    http_headers_w10_post = {
        'Host': f'{dest_addr}',
        'Connection': 'keep-alive',
        'Content-Length': len(http_payload),
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': f'http://{dest_addr}',
        'Referer': f'http://{dest_addr}/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7'
    }
    return http_request(http_method='POST', http_payload=http_payload, http_headers=http_headers_w10_post,
                        url=f'http://{dest_addr}', path='/answers/post')


def http_request(http_method='GET', http_fields=None, http_payload=None, http_headers=None, url=None, path='',
                 debug=True):
    if [_ for _ in (http_headers, url) if _ is None]:
        print(colored(f'PLS DEFINE:\n   http_headers: {http_headers}\n   url: {url}\n', 'red'))
    http = urllib3.PoolManager()
    if debug:
        print('------------------------------------------------------------------------------------')
        print(colored(f'Trying connect: {url}', 'green'))
        print(f'    Path: {path}')
        print(f'    Method: {http_method}')
        print(f'    Fields: {http_fields}')
        print(f'    Payload: {http_payload}')
        print(f'    Headers: {http_headers}')

    try:
        r = http.request(
            http_method,
            f'{url}{path}',
            fields=http_fields,
            body=http_payload,
            headers=http_headers,
            timeout=urllib3.Timeout(connect=1.0, read=1.0),
            retries=3
        )
        if debug:
            print(colored(f'\n    Response received: ', 'green'), colored(f'{r.data}', 'white'))
            print('------------------------------------------------------------------------------------')
        if r.status == 200:
            return json.loads(r.data.decode('utf-8'))
    except urllib3.exceptions.ConnectTimeoutError:
        print(colored('    Connection failed!!! Timeout error, check link or server availability...', 'red'))
        print('------------------------------------------------------------------------------------')
    except urllib3.exceptions.MaxRetryError:
        print(colored('    Connection retries failed!!! Check link or server availability...', 'red'))
        print('------------------------------------------------------------------------------------')
    except urllib3.exceptions.LocationValueError:
        print(colored(f'    Connection failed!!! Check ADDR: {ADDR} specified in {CONFIG}...', 'red'))
        print('------------------------------------------------------------------------------------')
