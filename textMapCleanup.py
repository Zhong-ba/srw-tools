import re
from config import CONFIG
import json


def replace_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        content = re.sub(r"\\\\n", "<br />", content)
        content = re.sub(r"<color=#f29e38ff>(.*?)</color>", r"{{Color|h|\1}}", content)
        content = re.sub(r"<color=#8790abff>(.*?)</color>", r"\1", content)
        content = re.sub(r"<unbreak>(.*?)</unbreak>", r"\1", content)
        content = re.sub(r"\{LAYOUT_MOBILE#Tap\}\{LAYOUT_CONTROLLER#Press\}\{LAYOUT_KEYBOARD#Click\}", r"(Tap/Press/Click)", content)
        content = re.sub(r"\{NICKNAME\}", r"(Trailblazer)", content)
        content = re.sub(r'\{RUBY_B#(.*?)\}(.*?)\{RUBY_E#\}', r'{{Rubi|\2|\1}}', content)
        content = re.sub(r'\{F#(.*?)\}\{M#(.*?)\}', r'{{MC|\2|\1}}', content)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Replacements completed and saved to {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
        
def merge_jsons(file1, file2, output_file):
    with open(file1, 'r', encoding = 'utf-8') as file:
        content1 = json.load(file)
        
    with open(file2, 'r', encoding = 'utf-8') as file:
        content2 = json.load(file)
        
    merged_content = content1
    merged_content.update(content2)
    
    with open(output_file, 'w', encoding = 'utf-8') as file:
        json.dump(merged_content, file, ensure_ascii = False, indent=2)
        

repl_langs = ["EN"]
repl_langs = ["CHS", "CHT", "ZHS", "ZHT", "DE", "EN", "ES", "FR", "ID", "JA", "JP", "KO", "KR", "PT", "RU", "TH", "VI", "TR", "IT"]
merge_langs = {
    "CHS": ["MainCHS", "CHS"],
    "CHT": ["MainCHT", "CHT"],
    "DE": ["MainDE", "DE"],
    "EN": ["MainEN", "EN"],
    "ES": ["MainES", "ES"],
    "FR": ["MainFR", "FR"],
    "ID": ["MainID", "ID"],
    "JP": ["MainJP", "JP"],
    "KR": ["MainKR", "KR"],
    "PT": ["MainPT", "PT"],
    "RU": ["MainRU", "RU"],
    "TH": ["MainTH", "TH"],
    "VI": ["MainVI", "VI"],
}

for lang, files in merge_langs.items():
    merge_jsons(f'{CONFIG["DataPath"]}/TextMap/TextMap{files[0]}.json', f'{CONFIG["DataPath"]}/TextMap/TextMap{files[1]}.json', f'{CONFIG["DataPath"]}/TextMap/TextMap{lang}.json')

for n in range(0, len(repl_langs)):
    replace_text(f'{CONFIG["DataPath"]}/TextMap/TextMap' + repl_langs[n] + ".json")
    
