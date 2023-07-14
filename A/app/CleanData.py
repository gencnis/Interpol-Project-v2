from pprint import pprint
import json

def clearData(data):
    """
    Clean the data by extracting relevant information from the input.

    Args:
        data (list): List of dictionaries containing the data to be cleaned.

    Returns:
        dict: Cleaned data in the desired format.


         example input: data = [{
                            'forename': 'RABIE', 
                            'date_of_birth': 
                            '1986/02/10', 
                            'entity_id': '2023/40891', 
                            'nationalities': ['DZ'], 
                            'name': 'RIFFI', 
                            '_links': {
                                'self': {...}, 
                                'images': {...}, 
                                'thumbnail': {...}
                                }
                            }, 
                            '_links': {
                                'self': {...}, 
                                'first': {...}, 
                                'last': {...}
                                }}
                            }

    example output: cleanData = {
                        1 : {
                            "name": "RIFFI",
                            "lastname": "RABIE",
                            "nationalities": ["DZ"],
                            "entity_id" : "2023/40891"
                            "date_of_birth": "1986/02/10",
                            "image": {...}  # Assuming there is a dictionary of image links here
                        },
                        "2": {
                            "name": "RIFFI",
                            "lastname": "RABIE",
                            "nationalities": ["DZ"],
                            "entity_id" : "2023/50891"
                            "date_of_birth": "1986/02/10",
                            "image": {...}  # Assuming there is a dictionary of image links here
                        },
                        ...
                    }
    """

    cleanData = {}
    id = 0

    for notice in data:
        entity_id = notice["entity_id"]

        if entity_id not in cleanData.values():
            # Extract image link from the _links section
            links = json.loads(notice['_links'].replace("'", '"'))
            image = links['images']['href']

            # Prepare cleaned data dictionary
            cleanData[id] = {
                'name': notice['name'],
                'lastname': notice['forename'],
                'nationalities': notice['nationalities'],
                'entity_id': notice['entity_id'],
                'date_of_birth': notice['date_of_birth'],
                'image': image
            }

        id += 1

    return cleanData


def main():
    # Example data for testing the clearData function
    example_data = [
        {
            1: {
                'forename': 'NİSA',
                'date_of_birth': '1986/2/10',
                'entity_id': '2023/40891',
                'nationalities': ['DZ'],
                'name': 'GENC',
                '_links': {
                    'self': {"hey"},
                    'images': {"image examp"},
                    'thumbnail': {"aaa"}
                }
            },
            '_links': {
                'self': {"i need this to work", 'please do work'},
                'first': {"hehe"},
                'last': {"lets see"}
            }
        },
        {
            'total': 10,
            'query': {
                'page': 1,
                'resultPerPage': 20,
                'nationality': 'AF'
            },
            '_embedded': {
                'notices': {
                    'forename': 'NİSA',
                    'date_of_birth': '1986/2/10',
                    'entity_id': '2023/50891',
                    'nationalities': ['DZ'],
                    'name': 'GENC',
                    '_links': {
                        'self': {"hey"},
                        'images': {"image examp"},
                        'thumbnail': {"aaa"}
                    }
                }
            },
            '_links': {
                'self': {"i need this to work", 'please do work'},
                'first': {"hehe"},
                'last': {"lets see"}
            }
        }
    ]

    pprint(clearData(example_data))


if __name__ == "__main__":
    main()
