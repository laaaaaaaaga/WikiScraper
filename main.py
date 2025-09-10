import wikipediaapi
import os
from urllib.parse import urljoin
MAX_FOLDER_SIZE = 1024*1024*1024
language_codes = ["en", "es", "fr", "de", "zh", "pt", "ru", "ja", "ko"]
more_language_codes = [
    "af", "als", "am", "an", "ar", "arc", "ary", "as", "ast", "atj",
    "av", "ay", "az", "ba", "bar", "bat-smg", "bcl", "be", "be-tarask",
    "bg", "bh", "bi", "bjn", "bm", "bn", "bo", "br", "bs", "bpy",
    "ca", "cbk-zam", "ce", "ceb", "ch", "chb", "chr", "chy", "co",
    "crh", "cs", "csb", "cu", "cv", "cy", "da", "de", "diq", "dsb",
    "dv", "dz", "el", "eml", "en", "eo", "es", "et", "eu", "ext",
    "fa", "fi", "frr", "fr", "fur", "fy", "ga", "gd", "gl", "gn",
    "go", "got", "grc", "gu", "gv", "he", "hi", "hif", "hr", "ht",
    "hu", "hy", "ia", "id", "ie", "ig", "ii", "ik", "ilo", "io",
    "is", "it", "iu", "ja", "jbo", "jv", "ka", "kbd", "kg", "ki",
    "kj", "kk", "kl", "km", "kn", "ko", "kr", "ksh", "ku", "kv",
    "kw", "ky", "la", "lb", "lez", "lfn", "lg", "li", "lij", "lip",
    "ln", "lo", "lt", "lv", "mai", "mg", "mh", "mi", "mk", "ml",
    "mn", "mr", "ms", "mt", "mwl", "my", "myv", "mzn", "na", "nb",
    "nd", "ne", "new", "ng", "niu", "nl", "nn", "no", "nov", "nrm",
    "nso", "nv", "oc", "oj", "om", "or", "os", "pa", "pag", "pap",
    "pcd", "pl", "ps", "pt", "qu", "rm", "rn", "ro", "ru", "rue",
    "rw", "sa", "sc", "sd", "se", "sg", "si", "sk", "sl", "smn",
    "sn", "so", "sq", "sr", "su", "sv", "sw", "ta", "te", "tg",
    "th", "ti", "tk", "tl", "to", "tpi", "tr", "ts", "tt", "tw",
    "ty", "ug", "uk", "ur", "uz", "ve", "vec", "vi", "vo", "wa",
    "wo", "xal", "yi", "yo", "za", "zh", "zu"]

import json
def save_to_json(path, data):
    with open(path, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_dir_size(directory):
    total_size = 0;
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            file_path = os.path.join(dirpath, f)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size


def init_wiki(lang):
    return wikipediaapi.Wikipedia(
    user_agent="WikiScraperBot/0.1 (marcingrelak6@gmail.com;) wikipediaapi/0.8.1",
    language=lang,
    extract_format=wikipediaapi.ExtractFormat.WIKI
    )


'''
def download_page(title, lang, dir):
    wiki = init_wiki(lang)
    
    page = wiki.page(title)
    if page.exists():
        path = os.path.join(dir, f"{page.title}_{lang}.txt")
        with open(path, "wb", encoding='utf-8') as file:
            file.write(page.text.encode('utf-8'))
        print("downloaded" f"{page.title}_{lang}")
    else:
        print("no page found")
#reminder that 10 gigabytes = 10*1024*1024*1024'''