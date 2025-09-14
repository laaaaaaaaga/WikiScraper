import wikipediaapi
import os
import requests

AGENT = "WikiScraperBot/1.1 (marcingrelak6@gmail.com;) wikipediaapi/0.8.1"
MAX_FOLDER_SIZE =  1024*1024*2# 3146084
language_codes = ["en", "es", "fr", "de", "zh", "pt", "ru", "ja", "ko"]
#excluded codes that have less than 1mb or are too long: "arc", "atj", "ay", "bar", "bat-smg", "be-tarask", "bi", "bm", "cbk-zam",
more_language_codes = ["af", "als", "am", "an", "ar", "ary", "as",
    "ast", "av", "az", "ba", "bcl", "be",
    "bg", "bh", "bjn", "bn", "bo", "br", "bs", "bpy",
    "ca", "ce", "ceb", "ch", "chb", "chr", "chy", "co",
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
        print("Folder {} created".format(path))

def get_dir_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            file_path = os.path.join(dirpath, f)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
#    print(total_size)
    return total_size


def init_wiki(lang):
    print("Initializing Wikipedia for language {}".format(lang))
    return wikipediaapi.Wikipedia(
        user_agent=AGENT,
        language=lang,
        timeout=(15, 160),
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )


def get_random_page_title(wiki):
    user_agent = AGENT
    try:
        response = requests.get(f'https://{wiki.language}.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&format=json', headers={'User-Agent': user_agent}, timeout=(15, 15))
        #first timer for request, second reader
    except requests.exceptions.ReadTimeout:
        print("read timeout error")
        return "Odessa Brigade"
    except requests.exceptions.Timeout:
        print("Timeout error")
        return "Odessa Brigade"
    except requests.exceptions:
        print("other exception error")
        return "Odessa Brigade"
    else:
        data = response.json()
        #print(data['query']['random'][0]['title'])
        return data['query']['random'][0]['title']

def save_page_content(wiki, page_title, directory):
    page = wiki.page(page_title)
    if not page.exists():
        return False
    file_path = os.path.join(directory, f"{page_title.replace(' ', '_').replace('\'', '').replace('/','_').replace('?','_').replace('*','_').replace('|','_').replace('\\','_').replace(':','_').replace('<','_').replace('>','_')}.txt")
    if os.path.exists(file_path):
        print("Page {} already exists".format(page_title))
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(page.text)
    return True

def download_pages(lang):
    try:
        wiki = init_wiki(lang)
        directory = f"{lang}_data"
        create_folder(directory)
        target_size = MAX_FOLDER_SIZE
        counter = 0

        while get_dir_size(directory) < target_size:
            page_title = get_random_page_title(wiki)
            if save_page_content(wiki, page_title, directory):
                #print(f"Saved: {page_title}")
                if os.path.exists(f"{directory}/{page_title.replace(' ', '_').replace('\'', '').replace('/','_').replace('?','_').replace('*','_').replace('|','_').replace('\\','_').replace(':','_').replace('<','_').replace('>','_')}.txt"):
                    counter+=1
                    print(f'{counter}" repeat in "{lang}')
                    if counter>2:
                        counter=0
                        break
            else:
                print(f"Page does not exist: {page_title}")
    except requests.exceptions.ReadTimeout:
        print("read timeout error")
    except requests.exceptions.Timeout:
        print("Timeout error")
    except:
        print("Something went wrong")
#maybe let's add exception with counter that if file exists already skip it, and if it happens 3 times in a row then it means we collected all. Price I pay for randomising instead of scraping links like i wanted earlier damn

def main():
    for l in more_language_codes:
        download_pages(l)

if __name__ == "__main__":
    print("program started")
    main()
    print("program ended")