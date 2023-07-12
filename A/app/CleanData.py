from pprint import pprint

def clearData(data):
    """
        Data is a list of dictionaries.
        example input: data = [{'total': 10, 
                                'query': {
                                    'page': 1, 
                                    'resultPerPage': 20, 
                                    'nationality': 
                                    'AF'}, 
                                '_embedded': {
                                    'notices': {
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
                                        }
                                    }, 
                                '_links': {
                                    'self': {...}, 
                                    'first': {...}, 
                                    'last': {...}
                                    }
                                }]

        example output: cleanData = {
                            "2023/40891": {
                                "name": "RIFFI",
                                "lastname": "RABIE",
                                "nationalities": ["DZ"],
                                "date_of_birth": "1986/02/10",
                                "image": {...}  # Assuming there is a dictionary of image links here
                            },
                            "2023/50891": {
                                "name": "RIFFI",
                                "lastname": "RABIE",
                                "nationalities": ["DZ"],
                                "date_of_birth": "1986/02/10",
                                "image": {...}  # Assuming there is a dictionary of image links here
                            },
                            ...
                        }
    """

    cleanData = {}
    unique_id = 0

    for item in data:
        notices = item["_embedded"]["notices"]

        for notice in notices:
            entity_id = notice["entity_id"]
            name = notice["name"]
            lastname = notice["forename"]
            date_of_birth = notice["date_of_birth"]
            nationalities = notice["nationalities"]
            image = notice["_links"]["images"]["href"]

            unique_identifier = (name, lastname, date_of_birth, tuple(nationalities))

            if unique_identifier not in cleanData:
                cleanData[unique_id] = {
                    "entity_id": entity_id,
                    "name": name,
                    "lastname": lastname,
                    "nationalities": nationalities,
                    "date_of_birth": date_of_birth,
                    "image": image
                }

                unique_id += 1
        
        print("Unique id baby girl: ", unique_id)

    return cleanData

def main():
    example_data = [
        {
            'total': 10, 
            'query': 
                {
                    'page': 1,  
                    'resultPerPage': 20,  
                    'nationality':  'AF'
                    
                },  
            '_embedded': 
                { 'notices': 
                    {
                        'forename': 'NİSA', 
                        'date_of_birth': '1986/2/10', 
                            'entity_id': '2023/40891', 
                            'nationalities': ['DZ'], 
                            'name': 'GENC', 
                            '_links': 
                                { 
                                    'self': 
                                        {
                                            "hey"
                                            
                                        }, 
                                    'images': 
                                        {
                                            "image examp"
                                            
                                        }, 
                                    'thumbnail': 
                                        {
                                            "aaa"
                                            
                                        }
                                    
                                }
                        
                    }
                    
                }, 
                '_links': 
                    { 
                        'elf': 
                            {
                                "i need this to work", 'please do work'
                                
                            }, 
                        'first': 
                            {
                                "hehe"
                                
                            }, 
                        'last': 
                            {
                                "lets see"
                            } 
                    }
            
        }, {
              'total': 10, 
            'query': 
                {
                    'page': 1,  
                    'resultPerPage': 20,  
                    'nationality':  'AF'
                    
                },  
            '_embedded': 
                { 'notices': 
                    {
                        'forename': 'NİSA', 
                        'date_of_birth': '1986/2/10', 
                            'entity_id': '2023/50891', 
                            'nationalities': ['DZ'], 
                            'name': 'GENC', 
                            '_links': 
                                { 
                                    'self': 
                                        {
                                            "hey"
                                            
                                        }, 
                                    'images': 
                                        {
                                            "image examp"
                                            
                                        }, 
                                    'thumbnail': 
                                        {
                                            "aaa"
                                            
                                        }
                                    
                                }
                        
                    }
                    
                }, 
                '_links': 
                    { 
                        'elf': 
                            {
                                "i need this to work", 'please do work'
                                
                            }, 
                        'first': 
                            {
                                "hehe"
                                
                            }, 
                        'last': 
                            {
                                "lets see"
                            } 
                    } 
        }]


    pprint(clearData(example_data))

if __name__ == "__main__":
    main()