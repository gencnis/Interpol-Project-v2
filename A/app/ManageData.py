"""
ManageData.py

This script extracts data from a given URL based on specified filters, cleans the data by removing unwanted entries or performing data 
    transformations, and produces the processed data for further analysis or usage.

The main steps of the script are as follows:
    1. Data Extraction: The script makes HTTP requests to the specified URL, applying various filters such as nationalities, genders, 
        age intervals, etc. The response is parsed as JSON, and the relevant data is extracted.

    2. Data Cleaning: The extracted data may contain irrelevant or inconsistent entries. The script applies cleaning operations,
        such as removing duplicates, formatting data, or removing unwanted information, to ensure the data is in a usable format.

    3. Data Processing: The cleaned data is processed further, if needed, to derive insights, perform calculations, or generate 
        additional derived data.

    4. Data Production: The processed data is outputted or stored in a desired format, such as CSV, JSON, or a database, for further 
        analysis, visualization, or integration with other systems.

The script relies on external modules and libraries such as requests, json, csv, and os for various functionalities. It utilizes functions 
    from custom modules like ExtractCountries, CleanData, and Producer to perform specific tasks.

@Author: Nisanur Genc

"""

from ExtractCountries import extract  # Import the extract function from ExtractCountries module
from CleanData import clearData  # Import the clearData function from CleanData module
from Producer import produce  # Import the produce function from Producer module
import requests  
import json 
from pprint import pprint  # Import the pprint function for pretty-printing data structures
import time 
import string  
import csv  
import os 

def extractData(url, nationalities, genders):
    """
    Extracts data from a given URL based on specified filters.

    Args:
        url (str): The URL to fetch data from.
        nationalities (list): List of nationalities to filter the data.
        genders (list): List of genders to filter the data.

    Returns:
        list: List of extracted data.
    """
    data = []  # Initialize an empty list to store the extracted data
    age_intervals = [  # Define a list of age intervals
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
            # Fetch data for each wantedBy nationality
            r = requests.get(url + "&arrestWarrantCountryId=" + wantedBy)
            r.raise_for_status()  # Raise an exception if the HTTP request fails
            response_text = r.text.replace("'", '"').decode('utf-8')  # Replace single quotes with double quotes and decode the response text
            response = json.loads(response_text)  # Parse the response text as JSON
            notices = response["_embedded"]["notices"]  # Extract the "notices" data from the response
            print("Ülkelerden istenen: ", wantedBy, response["total"])  # Print information about the wantedBy nationality

            if response["total"] > 160:
                for gender in genders:
                    try:
                        # Fetch data for each gender within the nationality
                        r = requests.get(url + "&arrestWarrantCountryId=" + wantedBy + "&sexId=" + gender)
                        r.raise_for_status()
                        response_text = r.text.replace("'", '"').decode('utf-8')
                        response = json.loads(response_text)
                        notices = response["_embedded"]["notices"]
                        print("Cinsiyetler ", gender, response["total"])

                        if response["total"] > 160:
                            for ageMin, ageMax in age_intervals:
                                try:
                                    # Fetch data for each age interval within the gender and nationality
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
                                                # Fetch data for each nationality within the gender, age interval, and nationality
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
                                                            # Fetch data for each letter within the nationality, gender, age interval, and nationality
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
                                                                        # Fetch data for each letter within the nationality, gender, age interval, nationality, and letter
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
                                                                    time.sleep(1)  # Add a delay to avoid overwhelming the server
                                                        except requests.exceptions.RequestException as e:
                                                            print(
                                                                f"Error occurred during the request for Soyadı {letter}: {str(e)}"
                                                            )
                                                            data.extend(notices)  
                                                            time.sleep(1)  # Add a delay to avoid overwhelming the server
                                            except requests.exceptions.RequestException as e:
                                                print(
                                                    f"Error occurred during the request for Ükesi {nation}: {str(e)}"
                                                )
                                                data.extend(notices)  
                                                time.sleep(1)  # Add a delay to avoid overwhelming the server
                                except requests.exceptions.RequestException as e:
                                    print(
                                        f"Error occurred during the request for Yaş {ageMin}-{ageMax}: {str(e)}"
                                    )
                                    data.extend(notices)
                                    time.sleep(1)  # Add a delay to avoid overwhelming the server
                    except requests.exceptions.RequestException as e:
                        print(
                            f"Error occurred during the request for Cinsiyetler {gender}: {str(e)}"
                        )
                        data.extend(notices)
                        time.sleep(1)  # Add a delay to avoid overwhelming the server
    except requests.exceptions.RequestException as e:
        print(
            f"Error occurred during the request: {str(e)}"
        )
        return None
    time.sleep(1)  # Add a delay to avoid overwhelming the server

    return data  # Return the extracted data

def print_stats(clean_data, data):
    """
    Prints statistics about the data.

    Args:
        clean_data (list): List of clean data.
        data (list): List of raw data.
    """
    pprint(clean_data)  # Pretty-print the clean data
    print("STATS: ")
    print("_______________________________________")
    print("\n List(data) uzunluğu: ", len(data))  # Print the length of the raw data list
    print("_______________________________________")
    print("\n Temiz veri sayısı: ", len(clean_data))  # Print the length of the clean data list
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
    """
    Read data from the CSV file and return a list of dictionaries.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: List of dictionaries representing the data.
    """
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
    print(os.getcwd())  # Print the current working directory
    file_path = "./app/data.csv"  # Specify the file path to read the data from
    data = read_data(file_path)  # Read the data from the CSV file
    # data = extractData(base_url, nationalities, genders)
    clean_data = clearData(data)  # Clean the data
    # print_stats(clean_data, data)
    # filename = 'data.csv'
    # write_data(data, filename)
    # write_data(clean_data, filename="clean_data.csv")
    produce(clean_data)  # Produce the processed data


if __name__ == "__main__":
    start_time = time.time()
    main()
    elapsed_time_minutes = (time.time() - start_time) / 60
    print(f"--- Requests and adding to the queue took {elapsed_time_minutes} minutes ---")
