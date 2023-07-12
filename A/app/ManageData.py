from ExtractCountries import extract
from CleanData import clearData
from Producer import produce
import requests
import json
from pprint import pprint
import time

def extractData(url, nationalities, genders):

    data = []

    for nation in nationalities:

        r = requests.get(url+"&nationality="+nation)
        response_text = r.text
        data_check = json.loads(response_text)

        print(nation, " bölgesi: ", data_check["total"], "veri.")

        if data_check["total"] != 0:

            if data_check["total"] > 160:

                for gender in genders:

                    r1 = requests.get(url+"&nationality="+nation+"&sexId="+gender)
                    response_text1 = r1.text
                    second_data_check = json.loads(response_text1)

                    if second_data_check["total"] > 160:

                        for wantedBy in nationalities:
                                
                            r2 = requests.get(url+"&nationality="+nation+"&sexId="+gender+"&arrestWarrantCountryId="+wantedBy)
                            response_text2 = r2.text
                            third_data_check = json.loads(response_text2)

                            if third_data_check["total"] > 160:
                                
                                for ageMin in range(18, 100):
                                
                                    r3 = requests.get(url+"&nationality="+nation+"&sexId="+gender+"&ageMin="+str(ageMin)+"&ageMax="+str(ageMin))
                                    response_text3 = r3.text
                                    data_dict = json.loads(response_text3)
                                    print("STATUS: ", r.status_code)

                                    if data_dict["total"] != 0:
                                        data.append(data_dict)

                            else:
                                data.append(third_data_check)
                    else:
                        data.append(second_data_check)
            else:
                data.append(data_check)

    return data
 

def print_stats(clean_data, data):

    total= 0
    for item in data:
        total= total+ item["total"] 
    
    pprint(clean_data)
    print("STATS: ")
    print("_______________________________________")
    print("\n List(data) uzunluğu: ", len(data))
    print("_______________________________________")
    print("\n Total veri sayısı: ", total)
    print("_______________________________________")
    print("\n Temiz veri sayısı: ", len(clean_data))
    print("_______________________________________")


def main():
    base_url = "https://ws-public.interpol.int/notices/v1/red?="
    nationalities = extract()
    genders = ["F", "M", "U"]

    data = extractData(base_url, nationalities, genders)
    clean_data = clearData(data)
    print_stats(clean_data, data)
    produce(clean_data)
    

if __name__ == "__main__":
    start_time = time.time()
    main()
    elapsed_time_minutes = (time.time() - start_time) / 60
    print(f"--- Requests and adding to the queue took {elapsed_time_minutes} minutes ---")