import string
from A.app.RabbitMQConnection import RabbitMQConnection
import time
from ExtractCountries import InterpolCountriesExtractor
import requests
import json

class InterpolDataExtractor:
    def __init__(self, rabbitmq_connection):
        self.rabbitmq_connection = rabbitmq_connection

    def clean_and_publish_data(self, notices):
        clean_data = []

        for notice in notices:
            entity_id = notice.get("entity_id")

            # Check if entity_id is not already present in clean_data
            if not any(item["entity_id"] == entity_id for item in clean_data):
                name = notice.get("name")
                lastname = notice.get("forename")
                date_of_birth = notice.get("date_of_birth")
                nationalities = notice.get("nationalities")
                image = notice.get("_links", {}).get("images", {})

                # Create a dictionary for this entity
                clean_item = {
                    "name": name,
                    "lastname": lastname,
                    "nationalities": nationalities,
                    "entity_id": entity_id,
                    "date_of_birth": date_of_birth,
                    "image": image,
                }

                # Publish the data to RabbitMQ
                try:
                    rabbitmq_connection.publish_data(clean_item)
                    print("Published data to RabbitMQ for entity ID:", entity_id)

                    # Append the clean item to the clean_data list
                    clean_data.append(clean_item)

                except Exception as e:
                    print("Error while publishing data for entity ID:", entity_id, e)

    
    
    def extract_by_wanted(self, nationalities, url):
        
        more_than_160 = []

        for wanted_by in nationalities:
            try:
                # Make the HTTP request
                r = requests.get(url + "&arrestWarrantCountryId=" + wanted_by)
                r.raise_for_status()  # Check for HTTP errors

                # Check for rate limit exceeded
                if "X-RateLimit-Remaining" in r.headers and int(r.headers["X-RateLimit-Remaining"]) == 0:
                    print("Rate limit exceeded. Retrying in a few minutes...")
                    time.sleep(60)  # Wait for a minute and retry
                    r = requests.get(url + "&arrestWarrantCountryId=" + wanted_by)  # Retry the request

                # Process the response data
                response = r.json()  # Parse the response as JSON

                # Check if the response data is as expected
                if "_embedded" in response and "notices" in response["_embedded"]:
                    notices = response["_embedded"]["notices"]
                    print("Ülkelerden istenen: ", wanted_by, response["total"])  # Print information about the wantedBy nationality

                    if response["total"] > 160:
                        more_than_160.append(wanted_by)

                    # Clean the data for the current nationality and append it to the main data list
                    self.clean_and_publish_data(notices)

                else:
                    print("Unexpected response format or missing data for nationality:", wanted_by)

            except requests.exceptions.RequestException as e:
                print("Error while fetching data for nationality:", wanted_by, e)
                # Handle connection errors, timeouts, etc.

            except json.JSONDecodeError as e:
                print("Error while parsing JSON response for nationality:", wanted_by, e)
                # Handle incomplete or unexpected data in the JSON response

            except requests.exceptions.HTTPError as e:
                print("HTTP error occurred for nationality:", wanted_by, e)
                # Handle specific HTTP status codes here (e.g., 404, 500)

            except Exception as e:
                print("An error occurred for nationality:", wanted_by, e)

            # Add a delay between requests to avoid rate limiting
            time.sleep(1)

        print("WantedBy nationalities with more than 160 entries:", more_than_160)
        return more_than_160



    def extract_by_gender(self, more_than_160_wanted, url):
        more_than_160 = []
        genders = ["U", "F", "M"]

        for wanted_by in more_than_160_wanted:
            for gender in genders:
                try:
                    # Make the HTTP request
                    r = requests.get(url + "&arrestWarrantCountryId=" + wanted_by + "&sexId=" + gender)
                    r.raise_for_status()  # Check for HTTP errors

                    # Check for rate limit exceeded
                    if "X-RateLimit-Remaining" in r.headers and int(r.headers["X-RateLimit-Remaining"]) == 0:
                        print("Rate limit exceeded. Retrying in a few minutes...")
                        time.sleep(60)  # Wait for a minute and retry
                        r = requests.get(url + "&arrestWarrantCountryId=" + wanted_by + "&sexId=" + gender)  # Retry the request

                    # Process the response data
                    response = r.json()  # Parse the response as JSON

                    # Check if the response data is as expected
                    if "_embedded" in response and "notices" in response["_embedded"]:
                        notices = response["_embedded"]["notices"]
                        print("Ülkelerden istenen: ", wanted_by, response["total"])  # Print information about the wantedBy nationality

                        if response["total"] > 160:
                            more_than_160.append((wanted_by, gender))

                        # Clean the data for the current nationality and append it to the main data list
                        self.clean_and_publish_data(notices)

                    else:
                        print("Unexpected response format or missing data for nationality:", wanted_by)

                except requests.exceptions.RequestException as e:
                    print("Error while fetching data for nationality:", wanted_by, e)
                    # Handle connection errors, timeouts, etc.

                except json.JSONDecodeError as e:
                    print("Error while parsing JSON response for nationality:", wanted_by, e)
                    # Handle incomplete or unexpected data in the JSON response

                except requests.exceptions.HTTPError as e:
                    print("HTTP error occurred for nationality:", wanted_by, e)
                    # Handle specific HTTP status codes here (e.g., 404, 500)

                except Exception as e:
                    print("An error occurred for nationality:", wanted_by, e)

                # Add a delay between requests to avoid rate limiting
                time.sleep(1)

            print("WantedBy nationalities with more than 160 entries:", more_than_160)

        return more_than_160

    def extract_by_age(self, more_than_160_genders, url):
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
        more_than_160 = []

        for wanted_by, gender in more_than_160_genders:
            for ageMin, ageMax in age_intervals:
                try:
                    # Make the HTTP request
                    r = requests.get(
                        url + "&arrestWarrantCountryId=" + wanted_by + "&sexId=" + gender +
                        "&ageMin=" + str(ageMin) + "&ageMax=" + str(ageMax)
                    )
                    r.raise_for_status()  # Check for HTTP errors

                    # Check for rate limit exceeded
                    if "X-RateLimit-Remaining" in r.headers and int(r.headers["X-RateLimit-Remaining"]) == 0:
                        print("Rate limit exceeded. Retrying in a few minutes...")
                        time.sleep(60)  # Wait for a minute and retry
                        r = requests.get(
                            url + "&arrestWarrantCountryId=" + wanted_by + "&sexId=" + gender +
                            "&ageMin=" + str(ageMin) + "&ageMax=" + str(ageMax)
                        )  # Retry the request

                    # Process the response data
                    response = r.json()  # Parse the response as JSON

                    # Check if the response data is as expected
                    if "_embedded" in response and "notices" in response["_embedded"]:
                        notices = response["_embedded"]["notices"]
                        print("Yaş ", ageMin, "-", ageMax, response["total"])  # Print information about the age interval

                        if response["total"] > 160:
                            more_than_160.append((wanted_by, gender, (ageMin, ageMax)))

                        # Clean the data for the current nationality and append it to the main data list
                        self.clean_and_publish_data(notices)

                    else:
                        print("Unexpected response format or missing data for age interval:", ageMin, "-", ageMax)

                except requests.exceptions.RequestException as e:
                    print("Error while fetching data for age interval:", ageMin, "-", ageMax, e)
                    # Handle connection errors, timeouts, etc.

                except json.JSONDecodeError as e:
                    print("Error while parsing JSON response for age interval:", ageMin, "-", ageMax, e)
                    # Handle incomplete or unexpected data in the JSON response

                except requests.exceptions.HTTPError as e:
                    print("HTTP error occurred for age interval:", ageMin, "-", ageMax, e)
                    # Handle specific HTTP status codes here (e.g., 404, 500)

                except Exception as e:
                    print("An error occurred for age interval:", ageMin, "-", ageMax, e)

                # Add a delay between requests to avoid rate limiting
                time.sleep(1)

        return more_than_160

    def extract_by_nationality(self, more_than_160_age, url, nationalities):
        more_than_160 = []
    
        for wantedBy, gender, age_interval in more_than_160_age:
            for ageMin, ageMax in age_interval:
                for nation in nationalities:
                    try:
                        # Make the HTTP request
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
                            more_than_160.append((wantedBy, gender, (ageMin, ageMax), nation))

                        # Clean the data for the current nationality and append it to the main data list
                        self.clean_and_publish_data(notices)

                    except requests.exceptions.RequestException as e:
                        print("Error while fetching data for nationality:", nation, e)
                        # Handle connection errors, timeouts, etc.

                    except json.JSONDecodeError as e:
                        print("Error while parsing JSON response for nationality:", nation, e)
                        # Handle incomplete or unexpected data in the JSON response

                    except requests.exceptions.HTTPError as e:
                        print("HTTP error occurred for nationality:", nation, e)
                        # Handle specific HTTP status codes here (e.g., 404, 500)

                    except Exception as e:
                        print("An error occurred for nationality:", nation, e)

                    # Add a delay between requests to avoid rate limiting
                    time.sleep(1)
        return more_than_160

    def extract_by_letter(self, more_than_160_nat, url):
        def make_request(wanted_by, gender, age_min, age_max, nation, letter, name=None):
            try:
                # Make the HTTP request
                params = {
                    "arrestWarrantCountryId": wanted_by,
                    "sexId": gender,
                    "ageMin": str(age_min),
                    "ageMax": str(age_max),
                    "nationality": nation,
                    "forename": letter,
                }

                if name is not None:
                    params["name"] = name

                r = requests.get(url, params=params)
                r.raise_for_status()

                response_text = r.text.replace("'", '"').decode('utf-8')
                response = json.loads(response_text)
                notices = response["_embedded"]["notices"]

                if name is None:
                    print("Soyadı", letter, response["total"])
                else:
                    print("Adı", name, response["total"])

                if response["total"] > 160:
                    if name is not None:
                        more_than_160.append((wanted_by, gender, (age_min, age_max), nation, letter, name))
                    else:
                        more_than_160.append((wanted_by, gender, (age_min, age_max), nation, letter))

                # Clean the data for the current nationality and append it to the main data list
                self.clean_and_publish_data(notices)

            except requests.exceptions.RequestException as e:
                print("Error while fetching data:", e)
                # Handle connection errors, timeouts, etc.

            except json.JSONDecodeError as e:
                print("Error while parsing JSON response:", e)
                # Handle incomplete or unexpected data in the JSON response

            except requests.exceptions.HTTPError as e:
                print("HTTP error occurred:", e)
                # Handle specific HTTP status codes here (e.g., 404, 500)

            except Exception as e:
                print("An error occurred:", e)

            # Add a delay between requests to avoid rate limiting
            time.sleep(1)
        
        more_than_160 = []

        for wanted_by, gender, age_interval, nation in more_than_160_nat:
            age_min, age_max = age_interval
            for letter in string.ascii_uppercase:
                make_request(wanted_by, gender, age_min, age_max, nation, letter)

                for fletter in string.ascii_uppercase:
                    make_request(wanted_by, gender, age_min, age_max, nation, letter, name=fletter)

        return more_than_160

    def start_extraction(self):
        while True:
            interpol_countries_extractor = InterpolCountriesExtractor("https://www.interpol.int/How-we-work/Notices/View-Red-Notices")
            nationalities = interpol_countries_extractor.get_extracted_nationalities()

            self.rabbitmq_connection.check_connection()

            try:
                base_url = "https://ws-public.interpol.int/notices/v1/red?="

                # Extract and clean the data
                more_than_160_wanted = self.extract_by_wanted(nationalities, base_url)
                more_than_160_gender = self.extract_by_gender(more_than_160_wanted, base_url)
                more_than_160_age = self.extract_by_age(more_than_160_gender, base_url)
                more_than_160_nat = self.extract_by_nationality(more_than_160_age, base_url, nationalities)
                more_than_160 = self.extract_by_letter(more_than_160_nat, base_url)
                print("You cannot get these: ", len(more_than_160))

            except Exception as e:
                print("Error in main:", e)

            time.sleep(1)

if __name__ == "__main__":
    rabbitmq_hostname = "rabbitmq"
    rabbitmq_port = 5672  # Default RabbitMQ port
    queue_name = "my_newQueue" 

    rabbitmq_connection = RabbitMQConnection(rabbitmq_hostname, rabbitmq_port, queue_name)
    rabbitmq_connection.connect()

    data_extractor = InterpolDataExtractor(rabbitmq_connection)
    data_extractor.start_extraction()
