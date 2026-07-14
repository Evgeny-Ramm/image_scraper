#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# image_scraper.py
# Скачивание изображений с цветным выводом, фильтром по формату и лимитом.

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
from colorama import init, Fore, Style

init(autoreset=True)

def download_image(url, folder, idx):
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = f"image_{idx}.jpg"
            filepath = os.path.join(folder, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"{Fore.GREEN}Скачано: {filename}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Не удалось скачать {url}{Style.RESET_ALL}")
    except Exception:
        print(f"{Fore.RED}Ошибка при скачивании {url}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="скачивание изображений")
    parser.add_argument("url", help="URL страницы")
    parser.add_argument("-o", "--output", default="images", help="папка для сохранения")
    parser.add_argument("--format", help="расширение (jpg, png, gif)")
    parser.add_argument("--limit", type=int, help="максимальное количество")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    try:
        response = requests.get(args.url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        img_urls = []
        for img in img_tags:
            src = img.get('src')
            if src:
                img_urls.append(urljoin(args.url, src))

        if args.format:
            img_urls = [u for u in img_urls if u.lower().endswith(f".{args.format.lower()}")]
        if args.limit:
            img_urls = img_urls[:args.limit]

        print(f"{Fore.CYAN}Найдено изображений: {len(img_urls)}{Style.RESET_ALL}")
        for i, url in enumerate(img_urls, 1):
            download_image(url, args.output, i)

        print(f"{Fore.GREEN}Готово!{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
