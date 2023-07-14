from ExtractCountries import extract
from CleanData import clearData
from Producer import produce
import requests
import json
from pprint import pprint
import time
import string
import csv
import os

import requests
import json
import string

def extractData(url, nationalities, genders):
    data = []
    age_intervals = [
        (18, 25),
        (25, 25),
        (26, 26),
        (27, 27),
        (28, 28),
        (29, 29),
        (30, 30),
        (31, 31),
        (32, 32),
        (33, 33),
        (34, 34),
        (35, 35),
        (36, 40),
        (40, 45),
        (45, 50),
        (50, 70),
        (70, 90),
        (90, 120)
    ]

    try:
        for wantedBy in nationalities:
            r = requests.get(url + "&arrestWarrantCountryId=" + wantedBy)
            r.raise_for_status()
            response_text = r.text.replace("'", '"').decode('utf-8')
            response = json.loads(response_text)
            notices = response["_embedded"]["notices"]
            print("Ülkelerden istenen: ", wantedBy, response["total"])

            if response["total"] > 160:
                for gender in genders:
                    try:
                        r = requests.get(url + "&arrestWarrantCountryId=" + wantedBy + "&sexId=" + gender)
                        r.raise_for_status()
                        response_text = r.text.replace("'", '"').decode('utf-8')
                        response = json.loads(response_text)
                        notices = response["_embedded"]["notices"]
                        print("Cinsiyetler ", gender, response["total"])

                        if response["total"] > 160:
                            for ageMin, ageMax in age_intervals:
                                try:
                                    r = requests.get(
                                        url + "&arrestWarrantCountryId=" + wantedBy + "&sexId=" + gender +
                                        "&ageMin=" + str(ageMin) + "&ageMax=" + str(ageMax)
                                    )
                                    r.raise_for_status()
                                    response_text = r.text.replace("'", '"').decode('utf-8')
                                    response = json.loads(response_text)
                                    notices = response["_embedded"]["notices"]
                                    print("Yaş ", ageMin, "-", ageMax, response["total"])

                                    if response["total"] > 160:
                                        for nation in nationalities:
                                            try:
                                                r = requests.get(
                                                    url + "&arrestWarrantCountryId=" + wantedBy + "&sexId=" + gender +
                                                    "&ageMin=" + str(ageMin) + "&ageMax=" + str(ageMin) +
                                                    "&nationality=" + nation
                                                )
                                                r.raise_for_status()
                                                response_text = r.text.replace("'", '"').decode('utf-8')
                                                response = json.loads(response_text)
                                                notices = response["_embedded"]["notices"]
                                                print("Ükesi ", nation, response["total"])

                                                if response["total"] > 160:
                                                    for letter in string.ascii_uppercase:
                                                        try:
                                                            r = requests.get(
                                                                url + "&arrestWarrantCountryId=" + wantedBy +
                                                                "&sexId=" + gender + "&ageMin=" + str(ageMin) +
                                                                "&ageMax=" + str(ageMin) + "&nationality=" + nation +
                                                                "&forename=" + letter
                                                            )
                                                            r.raise_for_status()
                                                            response_text = r.text.replace("'", '"').decode('utf-8')
                                                            response = json.loads(response_text)
                                                            notices = response["_embedded"]["notices"]
                                                            print("Soyadı ", letter, response["total"])

                                                            if response["total"] > 160:
                                                                for fletter in string.ascii_uppercase:
                                                                    try:
                                                                        r = requests.get(
                                                                            url + "&arrestWarrantCountryId=" + wantedBy +
                                                                            "&sexId=" + gender + "&ageMin=" + str(ageMin) +
                                                                            "&ageMax=" + str(ageMin) +
                                                                            "&nationality=" + nation +
                                                                            "&forename=" + letter + "&name=" + fletter
                                                                        )
                                                                        r.raise_for_status()
                                                                        response_text = r.text.replace("'", '"').decode('utf-8')
                                                                        response = json.loads(response_text)
                                                                        notices = response["_embedded"]["notices"]
                                                                        print("Adı ", fletter, response["total"])

                                                                    except requests.exceptions.RequestException as e:
                                                                        print(
                                                                            f"Error occurred during the request for Adı {fletter}: {str(e)}"
                                                                        )
                                                                    data.extend(notices) 
                                                                    time.sleep(1)
                                                        except requests.exceptions.RequestException as e:
                                                            print(
                                                                f"Error occurred during the request for Soyadı {letter}: {str(e)}"
                                                            )
                                                            data.extend(notices)  
                                                            time.sleep(1)
                                            except requests.exceptions.RequestException as e:
                                                print(
                                                    f"Error occurred during the request for Ükesi {nation}: {str(e)}"
                                                )
                                                data.extend(notices)  
                                                time.sleep(1)
                                except requests.exceptions.RequestException as e:
                                    print(
                                        f"Error occurred during the request for Yaş {ageMin}-{ageMax}: {str(e)}"
                                    )
                                    data.extend(notices)
                                    time.sleep(1)
                    except requests.exceptions.RequestException as e:
                        print(
                            f"Error occurred during the request for Cinsiyetler {gender}: {str(e)}"
                        )
                        data.extend(notices)
                        time.sleep(1)
    except requests.exceptions.RequestException as e:
        print(
            f"Error occurred during the request: {str(e)}"
        )
        return None
    time.sleep(1)

    return data

def print_stats(clean_data, data):
        
    pprint(clean_data)
    print("STATS: ")
    print("_______________________________________")
    print("\n List(data) uzunluğu: ", len(data))
    print("_______________________________________")
    print("\n Temiz veri sayısı: ", len(clean_data))
    print("_______________________________________")

def write_data(data, filename):
    """
    Writes data to a CSV file row by row.

    Args:
        data (list): List of dictionaries representing the data.
        filename (str): Name of the CSV file to create.

    Returns:
        bool: True if the data was successfully written to the CSV file, False otherwise.
    """
    if not data:
        return False

    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Write header row
            writer.writerow(data[0].keys())

            # Write data rows
            for item in data:
                row_values = [value.values() if isinstance(value, dict) else [value] for value in item.values()]
                writer.writerow(row_values)

        return True

    except IOError:
        return False
    
def read_data(file_path):
    """Read data from the CSV file and return a list of dictionaries.
        For the feature and testig purposes."""
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def main():
    # base_url = "https://ws-public.interpol.int/notices/v1/red?="
    # nationalities = extract()
    # genders = ["F", "M", "U"]
    print(os.getcwd())
    file_path = "./app/data.csv"
    data = read_data(file_path)
    # data = extractData(base_url, nationalities, genders)
    clean_data = clearData(data)
    # print_stats(clean_data, data)
    # filename = 'data.csv'
    # write_data(data, filename)
    # write_data(clean_data, filename="clean_data.csv")
    produce(clean_data)
    


if __name__ == "__main__":
    start_time = time.time()
    main()
    elapsed_time_minutes = (time.time() - start_time) / 60
    print(f"--- Requests and adding to the queue took {elapsed_time_minutes} minutes ---")
