import wikipediaapi
import os
from urllib.parse import urljoin

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_dir_size(path):
    total_size = 0;
    for filenames in os.walk(path):
        for f in filenames:
            total_size += os.path.getsize(os.path.join(dirpath, f))
            if not os.path.islink(os.path.join(dirpath, f)):
                total_size += os.path.getsize(os.path.join(dirpath, f))
    return total_size

def download_page(title, lang, dir):
    wiki = wikipediaapi.Wikipedia(lang, user_agent="WikiScraper/0.1 (marcingrelak6@gmail.com) wikipediaapi/0.8.1")
    page = wiki.page(title)
    if page.exists():
        path = os.path.join(dir, f"{page.title}_{lang}.txt")
        with open(path, "wb", encoding='utf-8') as file:
            file.write(page.content)
        print("downloaded" f"{page.title}_{lang}")
    else:
        print("no page found")