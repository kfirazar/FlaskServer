import dataclasses 
import requests 
import json



@dataclasses.dataclass
class Shop_Data:
    shop_name : str
    access_token : str

    API_VERSION = '2024-04'
    def __init__(self,shop_name) -> None:
        self.shop_name = shop_name
        self.access_token = '' #Extracted from db
        
    @property
    def shop_products_url(self):
        return f"https://{self.shop_name}.myshopify.com/admin/api/{Shop_Data.API_VERSION}/products.json"
    
    
    @property
    def shop_header_auth(self):
        return { 
            "X-Shopify-Access-Token" : f"{self.access_token}",
            "Content-Type" : "application/json"
        }


    
    """
    -----------------------------------------------
        Extract data from Db:
        shop_url     -> SHOP_NAME 
        headers      -> ADMIN_KEY
        product_data -> extract from the FORM in app.py via ___
    -----------------------------------------------
    """

    
    def create_product(self,json_data=None):
        """
        ----------------------------------------------------------------------------
            Purpose  -> Creates a product in the Shopify store.
        
            Args     -> Json_data (dict): JSON data of the product to be created.
        
            Raises   -> ValueError: If json_data is not provided.
        ----------------------------------------------------------------------------
        """
        
        headers = self.shop_header_auth
        shop_url = self.shop_products_url
        if json_data == None:
            raise ValueError("Missing product data")


        response = requests.post(url=shop_url,headers=headers,json=json_data)
        if response.status_code == 201:
            print('Product Uploaded Successfully')
        else:
            print(f"Error: {response.status_code} - {response.text}")
            """
            -------------------------------------------------------------------
                Add : Send notification to the user there was an error
            -------------------------------------------------------------------
            """
       
shop_name = 'testqwerfe4r4'
file_path = r'C:\Users\kfirs\Documents\FlaskProject\FlaskServer\Db\db.json'

# Load JSON file
with open(file_path, 'r') as file:
    data = json.load(file)
    data = data[shop_name]
    
shop = Shop_Data(shop_name)

#Not working - correcting the format#
for product in data:
    shop.create_product(data[product])

