import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import itertools
import httpx
import asyncio
domain = "https://t.me/addstickers/"
supported_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_']
first_supported_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
counter = 0

def _log(text):
    print("[{}] {}".format(datetime.now(), text))
    with open('D:\\test\\tg_stickers_brute_force\\logs.log', 'a', encoding='utf-8') as l:
        l.write("[{}] {}\n".format(datetime.now(), text))

def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def check_if_exists(response) -> str | False:
    try:

        stick = BeautifulSoup(response, 'lxml').find('div', class_="tgme_page_description")
        get_name_raw = re.search('(?:the \<strong\>)(.+)(?:\<\/strong\> sticker set\.)', str(stick))
        if get_name_raw is None:
            return False
        else:
            get_name = get_name_raw.group(1).strip()
            return get_name
    except Exception as e:
        _log(f"Error {e}, sleeping")
        time.sleep(1)
        return False

async def run_async_per_word_bruteforce():
    global counter
    with open("D:\\test\\word_list.txt", "r") as f:
        word_list = [word.strip() for word in f.readlines()]
    urls = []
    for word in word_list:
        word = re.sub(r"[^\w]", "", word)
        if word:
            if len(word) >= 5:
                urls.append(domain + word)
            else:
                urls.append(domain + word * (5//len(word) + 1))
    _log(f"Urls prepared, length: {len(urls)}, removed {len(word_list)-len(urls)} words")
    chunked_list = list(_chunks(urls, 100))
    
    _log(f"chunked list created, running async code for each!")
    for link_chunk in chunked_list:
        async with httpx.AsyncClient() as client:
            tasks = (client.get(url) for url in link_chunk)
            reqs = await asyncio.gather(*tasks)
        for req in reqs:
            if check := check_if_exists(req.text):
                _log(f"Found sticker set #{counter}, \"{check}\" with the link of {req.url}")


    

def run_characters_bruteforce():
    global counter
    for i in range(3,len(first_supported_chars)):
        result_list = itertools.product(supported_chars, repeat=5)
        for result_item in result_list:
            result = domain + first_supported_chars[i] + result_item
            
            counter = counter+1
            response = requests.get(result).text
            check = check_if_exists(response)
            if check:
                _log("Found sticker set #{}, \"{}\" with the link of {}".format(counter, check, result))

def run_per_word_bruteforce():
    global counter
    with open("D:\\test\\word_list.txt", "r") as f:
        word_list = f.read().split().strip()
    for word in word_list:
        word = re.sub(r"^[^A-Za-z][^\w]", "", word)
        if len(word) < 5:
            result = domain + word * (5//len(word))
        else:
            result = domain + word
        counter += 1
        response = requests.get(result).text
        if check := check_if_exists(response):
            _log("Found sticker set #{}, \"{}\" with the link of {}".format(counter, check, result))
        
             


# def run():
#     global counter
#     for i in range(3,len(first_supported_chars)):
#         result = ''
#         for k in range(len(supported_chars)):
#             for j in range(len(supported_chars)):
#                 for l in range(len(supported_chars)):
#                     for p in range(len(supported_chars)):
#                         result = domain + first_supported_chars[i] + supported_chars[k] + supported_chars[j] + supported_chars[l] + supported_chars[p]
#                         counter = counter+1
#                         check = check_if_exists(result)
#                         if check:
#                             _log("Found sticker set #{}, \"{}\" with the link of {}".format(counter, check, result))



if __name__ == '__main__':
    _log("====LOG BEGIN====")
    asyncio.run(run_async_per_word_bruteforce())