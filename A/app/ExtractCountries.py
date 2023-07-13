import requests
from bs4 import BeautifulSoup

def extract():
    """
    Extracts the list of nationalities from the Interpol website.

    Returns:
        list: A list of nationalities extracted from the website.
    """
    nationality_list = []

    # Send a GET request to the Interpol website and parse the HTML content
    html = requests.get("https://www.interpol.int/How-we-work/Notices/View-Red-Notices")
    content = BeautifulSoup(html.text, "html.parser")

    # Find the select element with the name "nationality" and get all option elements
    options = content.find("select", {"name": "nationality"}).findAll("option")

    # Iterate over the option elements and extract the values (nationalities)
    for opt in options:
        # Check if the option has a 'value' attribute
        if opt.has_attr('value'):
            nationality_list.append(opt['value'])

    return nationality_list

if __name__ == "__main__":
    # Extract the list of nationalities
    nationality_list = extract()
