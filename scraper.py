#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse

def download_image(url, folder):
    """Скачивает изображение по URL и сохраняет в папку folder."""
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            # Определяем имя файла из URL
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = "image.jpg"
            # Полный путь для сохранения
            filepath = os.path.join(folder, filename)
            # Сохраняем изображение
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Скачано: {filename}")
        else:
            print(f"Не удалось скачать {url} (статус {response.status_code})")
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")

def get_images_from_page(url):
    """Парсит страницу, находит все теги <img> и возвращает список URL изображений."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        img_urls = []
        for img in img_tags:
            src = img.get('src')
            if src:
                # Преобразуем относительный URL в абсолютный
                absolute_url = urljoin(url, src)
                img_urls.append(absolute_url)
        return img_urls
    except Exception as e:
        print(f"Ошибка при загрузке страницы {url}: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Скачивает все изображения с веб-страницы")
    parser.add_argument("url", help="URL страницы для парсинга")
    parser.add_argument("-o", "--output", default="images", help="Папка для сохранения (по умолчанию 'images')")
    args = parser.parse_args()

    # Создаём папку для изображений, если её нет
    os.makedirs(args.output, exist_ok=True)

    print(f"Парсинг страницы: {args.url}")
    img_urls = get_images_from_page(args.url)
    print(f"Найдено изображений: {len(img_urls)}")

    for img_url in img_urls:
        download_image(img_url, args.output)

    print("Готово!")

if __name__ == "__main__":
    main()
