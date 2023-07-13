from ExtractCountries import extract
from CleanData import clearData
from Producer import produce
import requests
import json
from pprint import pprint
import time
import string
import csv

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
    (90, 120)]

    for wantedBy in nationalities:
        r = requests.get(url+"&arrestWarrantCountryId="+wantedBy)
        response_text = r.text
        response = json.loads(response_text)
        notices = response["_embedded"]["notices"]
        print("Ülkelerden istenen: ", wantedBy, response["total"])

        if response["total"] > 160:
            
            for gender in genders:

                r = requests.get(url+"&arrestWarrantCountryId="+wantedBy+"&sexId="+gender)
                response_text = r.text
                response = json.loads(response_text)
                notices = response["_embedded"]["notices"]
                print("Cinsiyetler ", gender, response["total"])


                if response["total"] > 160:
                     
                    # for ageMin in range(18, 100):
                    #     r = requests.get(url+"&arrestWarrantCountryId="+wantedBy+"&sexId="+gender+"&ageMin="+str(ageMin)+"&ageMax="+str(ageMin))
                    #     response_text = r.text
                    #     response = json.loads(response_text)
                    #     notices = response["_embedded"]["notices"]
                    #     print("Yaş ", ageMin, response["total"])

                    for ageMin, ageMax in age_intervals:
                        r = requests.get(url+"&arrestWarrantCountryId="+wantedBy+"&sexId="+gender+"&ageMin="+str(ageMin)+"&ageMax="+str(ageMax))
                        response_text = r.text
                        response = json.loads(response_text)
                        notices = response["_embedded"]["notices"]
                        print("Yaş ", ageMin, "-", ageMax, response["total"])
                     
                     
                        if response["total"] > 160:
                             
                            for nation in nationalities:
                                r = requests.get(url+"&arrestWarrantCountryId="+wantedBy+"&sexId="+gender+"&ageMin="+str(ageMin)+"&ageMax="+str(ageMin)+"&nationality="+nation)
                                response_text = r.text
                                response = json.loads(response_text)
                                notices = response["_embedded"]["notices"]
                                print("Ükesi ", nation , response["total"])

                                if response["total"] > 160:

                                    for letter in string.ascii_uppercase:
                                        r = requests.get(url+"&arrestWarrantCountryId="+wantedBy+"&sexId="+gender+"&ageMin="+str(ageMin)+"&ageMax="+str(ageMin)+"&nationality="+nation+"&forename="+letter)
                                        response_text = r.text
                                        response = json.loads(response_text)
                                        notices = response["_embedded"]["notices"]
                                        print("Soyadı ", letter, response["total"])

                                        if response["total"] > 160:

                                            for fletter in string.ascii_uppercase:
                                                    r = requests.get(url+"&arrestWarrantCountryId="+wantedBy+"&sexId="+gender+"&ageMin="+str(ageMin)+"&ageMax="+str(ageMin)+"&nationality="+nation+"&forename="+letter+"&name="+fletter)
                                                    response_text = r.text
                                                    response = json.loads(response_text)
                                                    notices = response["_embedded"]["notices"]
                                                    print("Adı ", fletter, response["total"])

                                                    data.extend(notices)
                                        data.extend(notices)
                                data.extend(notices)
                        data.extend(notices)
                data.extend(notices)
        data.extend(notices)

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

def main():
    base_url = "https://ws-public.interpol.int/notices/v1/red?="
    nationalities = extract()
    genders = ["F", "M", "U"]

    data = extractData(base_url, nationalities, genders)
    clean_data = clearData(data)
    print_stats(clean_data, data)
    filename = 'data.csv'
    write_data(data, filename)
    write_data(clean_data, filename="clean_data.csv")
    produce(clean_data)
    


if __name__ == "__main__":
    start_time = time.time()
    main()
    elapsed_time_minutes = (time.time() - start_time) / 60
    print(f"--- Requests and adding to the queue took {elapsed_time_minutes} minutes ---")
