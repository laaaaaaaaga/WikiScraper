import wikipediaapi
import os
from urllib.parse import urljoin

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

#ommitting folders since crawler will only create files
def get_dir_size(dir):
    total_size = 0;
    for dirpath, dirnames, filenames in os.walk(dir):
        for f in filenames:
            file_path = os.path.join(dirpath, f)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size

def download_page(title, lang, dir):
    wiki = wikipediaapi.Wikipedia(
    user_agent="WikiScraperBot/0.1 (marcingrelak6@gmail.com) wikipediaapi/0.8.1",
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    page = wiki.page(title)
    if page.exists():
        path = os.path.join(dir, f"{page.title}_{lang}.txt")
        with open(path, "wb", encoding='utf-8') as file:
            file.write(page.text.encode('utf-8'))
        print("downloaded" f"{page.title}_{lang}")
    else:
        print("no page found")