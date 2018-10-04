"""
Необходимо написать скрипт, выполняющий рекурсивный обход сайта(для тестов
используйте mosigra.ru и www.csd.tsu.ru) и вывести без дубликатов все адреса
электронной почты содержащиеся на страницах. Для ускорения работы - добавьте
ограничитель на переходы(напр. 10) по ссылкам - сайт может содержать очень
много страниц.

Для извлечения email и url следует использовать регулярные выражения.

Базовый язык - Python 2.7 или Python 3.5. Требуется использовать библиотеки
requests для http запросов и re для RegEx.

Задание на языке python требуется сдать до 23:59 (UTC+7) 1 Ноября.
"""

import requests
import re

URL_1 = "https://mosigra.ru"
URL_2 = "http://www.csd.tsu.ru"

DEEP = 10

def parse_links_from_text(url, text):
    if 'https' in url:
        url_trailed = re.sub(r'https://', '', url)
    elif 'http' in url:
        url_trailed = re.sub(r'http://', '', url)

    regex = r'' + url_trailed + r'[\/\_\-\:\.a-zA-Z0-9]+'
    pattern = re.compile(regex)
    results = pattern.findall(text)

    if 'https' in url:
        results_with_protocol = list(map(lambda x: 'https://' + x, results))
    elif 'http' in url:
        results_with_protocol = list(map(lambda x: 'http://' + x, results))
    return set(results_with_protocol)

def parse_emails_from_text(text):
    regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    pattern = re.compile(regex)
    results = pattern.findall(text)
    return set(results)

def find_emails_from_url(url, deep):
    visited_pages = set()
    links = set()
    emails = set()
    recursive_find_emails_from_url(url, deep, visited_pages, links, emails)
    return (links, emails)


def recursive_find_emails_from_url(url, deep, visited_pages, links, emails):
    try:
        page = requests.get(url)
    except requests.exceptions.RequestException:
        print("Bad url: " + url)
        return

    visited_pages.add(url)
    new_links = parse_links_from_text(url, page.text)
    links |= new_links
    new_emails = parse_emails_from_text(page.text)
    emails |= new_emails

    if deep > 0:
        for link in new_links:
            if link in visited_pages:
                continue
            else:
                recursive_find_emails_from_url(link, deep - 1, visited_pages, links, emails)

def main():
    links, emails = find_emails_from_url(URL_1, DEEP)
    # print("===== LINKS =====")
    # print(links)
    # print(len(links))
    print("===== EMAILS =====")
    print(emails)
    print(len(emails))

if __name__ == '__main__':
    main()
