#PoC#
import dataclasses
import json
import os.path
import dataclasses

"""
--------------------------------------------------------------------------------
    NOTE : It is PoC so not very BASIC and UNTRADIONALL db stracture
--------------------------------------------------------------------------------
"""

@dataclasses.dataclass
class DbConnect:
    path: str = dataclasses.field(init=False, default="Db/db.json")
    
    """
    --------------------------------------------------------------------------------------
        Purpose -> open handler for file AUTOMATICALLY after instance creation
    --------------------------------------------------------------------------------------
    """

    def __post_init__(self) -> None:
        self.file_handle = open(self.path, 'a')        

    def close_db(self) -> None:
        self.file_handle.close()
    
    
    """
    ---------------------------------------------------
        Purpose    -> extract current data stored

        Args       -> None

        Exeception -> None
    ---------------------------------------------------
    """
    def read_json(self) -> json:
        # Open the file in read mode
        with open(self.path, 'r') as file:
            try:
                # Load and return the JSON data
                return json.load(file)
            except json.JSONDecodeError:
                # If the file is empty or not a valid JSON, return an empty dictionary
                return {}
            
    
    def get_products_by_shop(self,shop_name) ->json:
        json_data = self.read_json()
        try:
            val =  json_data[shop_name]
        except:
            val ={}
        finally:
            return val

    

  
     
    def write_to_db(self, shop_name: str, data: dict) -> None:
        """
        -----------------------------------------------------------------
            Purpose     -> Write data into db

            Requirement -> A store MUST be initialize in db

            Q&A:
            -Where does STORE enter db?-
                ->In manager side, where he can publish his store.
        -----------------------------------------------------------------
        """
        current_data = self.read_json()
        if shop_name not in current_data:
            raise ValueError(f"Store '{shop_name}' is not initialized in the database.")
            
        # Update the existing data with new data
        current_data[shop_name].update(data)
        print(current_data)
        with open(self.path, 'w') as file:
            """
            --------------------------------------------------------------------------
                Json.dump:
                    Used when you want to save JSON data to a file.
    
                Json.dumps:
                    Used when you want to work with JSON data as a string,
                    perhaps for further processing or network transmission.
            --------------------------------------------------------------------------
            """
            json.dump(current_data, file, indent=4)

    
# Example of how to use the class
