import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import itertools
domain = "https://t.me/addstickers/"
supported_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_']
first_supported_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
counter = 0

def _log(text):
    print("[{}] {}".format(datetime.now(), text))
    logs.write("[{}] {}\n".format(datetime.now(), text))

def check_if_exists(link):
    try:
        response = requests.get(link).text
        stick = BeautifulSoup(response, 'lxml').find('div', class_="tgme_page_description")
        get_name_raw = re.search('(?:the \<strong\>)(.+)(?:\<\/strong\> sticker set\.)', str(stick))
        if get_name_raw is None:
            return False
        else:
            get_name = get_name_raw.group(1).strip()
            return get_name
    except Exception as e:
        _log("Error " + str(e) + " at link \"" + link + "\"")
        time.sleep(1)
        return False


        

def run_characters_bruteforce():
    global counter
    for i in range(3,len(first_supported_chars)):
        result_list = itertools.product(supported_chars, repeat=5)
        for result_item in result_list:
            result = domain + first_supported_chars[i] + result_item
            
            counter = counter+1
            check = check_if_exists(result)
            if check:
                _log("Found sticker set #{}, \"{}\" with the link of {}".format(counter, check, result))

def run_per_word_bruteforce():
    global counter
    with open("D:\\test\\word_list.txt", "r") as f:
        word_list = f.read().split()
    for word in word_list:
        word = re.sub(r"^[^A-Za-z][^\w]", "", word)
        if len(word) < 5:
            result = domain + word * (5//len(word))
        else:
            result = domain + word
        counter += 1
        if check := check_if_exists(result):
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
    logs = open('D:\\test\\tg_stickers_brute_force\\logs.log', 'w', encoding='utf-8')
    logs.write("====LOG BEGIN====\n")
    run_per_word_bruteforce()
    logs.close()