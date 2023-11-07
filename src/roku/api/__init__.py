
from typing import OrderedDict, Any
import xmltodict
import requests
import sys
from requests import Response

requests.packages.urllib3.disable_warnings()

KEYS = {  
    "Home",
    "Rev",
    "Fwd",
    "Play",
    "Select",
    "Left",
    "Right",
    "Down",
    "Up",
    "Back",
    "InstantReplay",
    "Info",
    "Backspace",
    "Search",
    "Enter"
}

KEYBOARD_PREFIX = "Lit_"

# https://codereview.stackexchange.com/questions/185966/functions-to-convert-camelcase-strings-to-snake-case
def to_snake_case(input_string: str) -> str:
  """Camel case to joint-lower"""

  new_string = input_string[0].lower()
  for i, letter in enumerate(input_string[1:], 1):
    if letter.isupper():
      if input_string[i-1].islower() or (i != len(input_string)-1 and input_string[i+1].islower()):
        new_string += '_'
    new_string += letter.replace('-', '_').lower()
  return new_string

def remap_keys(ugly_dict: dict) -> dict:
   return {to_snake_case(k):v for k,v in ugly_dict.items()}

def base_response(url: str) -> (Response|None):
    response = None
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
    except requests.exceptions.Timeout as error:
        print("Timeout", error)
        sys.exit(1)
    except requests.exceptions.TooManyRedirects as error:
        print("TooManyRedirects", error)
        sys.exit(1)
    except requests.exceptions.HTTPError as error:
        print("HTTP Error encountered", error)
        sys.exit(1)
    except requests.exceptions.ConnectionError as error:
        print("Connection Error", error) 
    return response

def post_response(url: str):
    response = None
    try:
        response = requests.post(url, timeout=3, data="")
        response.raise_for_status()
    except requests.exceptions.Timeout as error:
        print("Timeout", error)
        sys.exit(1)
    except requests.exceptions.TooManyRedirects as error:
        print("TooManyRedirects", error)
        sys.exit(1)
    except requests.exceptions.HTTPError as error:
        print("HTTP Error encountered", error)
        sys.exit(1)
    except requests.exceptions.ConnectionError as error:
        print("Connection Error", error) 
    return response  

def parse_response(response: Response) -> OrderedDict[str, Any]:
    return xmltodict.parse(response.text)

def get_root(ip: str, port: int) -> OrderedDict[str, Any]:
    base_url = f"http://{ip}:{port}/"
    return parse_response(base_response(base_url))

def device_info(ip: str, port: int = 8060):
    return remap_keys(get_root(ip, port)['root']['device'])

def query_apps(ip: str, port: int = 8060):
    return parse_response(base_response(f"http://{ip}:{port}/query/apps"))['apps']['app']

def query_media_player(ip: str, port: int = 8060):
    return parse_response(base_response(f"http://{ip}:{port}/query/media-player"))

def query_device_info(ip: str, port: int = 8060):
    return remap_keys(parse_response(base_response(f"http://{ip}:{port}/query/device-info"))['device-info'])

def query_chanperf(ip: str, port: int = 8060):   
    return parse_response(base_response(f"http://{ip}:{port}/query/chanperf"))

def keydown(ip: str, r_key: str, port: int = 8060):
    return parse_response(post_response(f"http://{ip}:{port}/keydown/{r_key}"))

def keyup(ip: str, r_key: str, port: int = 8060):
    return parse_response(post_response(f"http://{ip}:{port}/keyup/{r_key}"))

def keypress(ip: str, r_key: str, port: int = 8060):
    return parse_response(post_response(f"http://{ip}:{port}/keypress/{r_key}"))

