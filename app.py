from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


from Db.db_connect import DbConnect
from datetime import datetime
import json

@app.route('/', methods=['POST', 'GET'])
def index():
    """
    ------------------------------------------------------------------------------------------------
        Requrirment      -> Need to be signed in + selected shop

        Purpose          -> Handle GET and POST requests to the index route.

        Returns          -> On GET request: Renders the index.html template.
    .                    -> On POST request: Returns a JSON response containing the extracted data -> sent to be validate and handle
    ------------------------------------------------------------------------------------------------            
    """

    if request.method == 'POST':
        print(request)
        if request.is_json:
            data = request.get_json()  # Parse the incoming JSON request data
        else:
            data = request.form.to_dict()  # Handle form submission if JSON is not received
        
        """
        ---------------------------------------------------------------------------
          ADD Check for the different attribute for validating the info 
          Notice : XSS , SqlInjection etc...
        ---------------------------------------------------------------------------
        """

        #Data needs to be extracted 
        title = data.get('title')
        body_html = data.get('body_html')
        sku = data.get('sku')
        supplier = data.get('supplier')

        with open('C:\Users\kfirs\Documents\FlaskProject\FlaskServer\product.json', 'r') as file:
            data = json.load(file)

        """
        -------------------------------------------------------------------------------------------------------------------
            Purpose -> Create a class that is intermediary who convert raw data to correct format of product.json
        -------------------------------------------------------------------------------------------------------------------
        """

        response_data = {
            
            datetime.now().strftime('%Y/%m/%d %H:%M:%S') : {
                'title': title,
                'body_html': body_html,
                'sku': sku,
                'supplier': supplier
            }
        }
       
        """
        ---------------------------------------------------------------------------
            1.Store the product -> db. 
                Requrirment : Admin verfication(=Shop Owner)
            2.Accepted
                2.1.USE the response_data + shop_data.py -> Upload the product
        ---------------------------------------------------------------------------
        """
        db = DbConnect()

        """
        ---------------------------------------------------------------------------
            Add -> validation process for finding error/problem in the data 
        ---------------------------------------------------------------------------
        """
        print(response_data)
        db.write_to_db("testqwerfe4r4",response_data)
        db.close_db()

        #return jsonify(response_data)  # Return a JSON response

    # Render the index.html template for GET requests    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

