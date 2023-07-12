import requests
from bs4 import BeautifulSoup

def extract():
    nationality_list = []

    html = requests.get("https://www.interpol.int/How-we-work/Notices/View-Red-Notices")
    content = BeautifulSoup(html.text, "html.parser")

    options = content.find("select", {"name": "nationality"}).findAll("option")

    for opt in options:
        if opt.has_key('value'):
            nationality_list.append(opt['value'])

    return nationality_list

if __name__ == "__main__":
    nationality_list = extract()