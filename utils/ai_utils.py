import ast
from PIL import Image as PILImage
import requests
import base64


def analyze_receipt_image(image_path):
    """
    Analyzes an image of a receipt using Google Generative AI and extracts information.

    Args:
        image_path:  Path to the receipt image file (e.g., "receipt.jpg").

    Returns:
        str: A string containing the analysis result from the model.  If there's an error,
             it returns an error message.
    """
    try:
        GOOGLE_API_KEY = 'AIzaSyB-lE7DY_eKwATeWjznVX_klfrhaKfscGw'

        if not GOOGLE_API_KEY:
            print("Error: Google API key not found.   Please set the GOOGLE_API_KEY environment variable.")
            exit()

        # Construct the prompt
        prompt = """
        You are an expert receipt analyzer.  Your task is to extract all relevant
        information from the receipt image provided.  Specifically, look for:

        - Merchant Name (business where the purchase was made)
        - Date of Purchase . Present this information in format DD/MM/YYYY
        - Total Amount
        - List of Items Purchased (if possible, include quantity and price per item) Present this information in format {"item": item_name, "quantity": quantity, "price": price}. If the quantity is not specified, assume the quantity is 1.

        Present the information in a clear and organized format in an python object without any comments and without new lines (\n), so only the raw object. All the words should be lower case. If some information
        is not available in the image, indicate that it is "Not Found".
        """        

        # Generate content (analyze the image and respond to the prompt)
        # Read and encode the image
        with open(image_path, "rb") as img_file:
            image_bytes = img_file.read()
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "contents": [{
                "parts": [{"inlineData": 
                           {"mimeType": "image/jpeg", "data": image_b64}},
                          {"text": prompt}]
            }]
        }
        response = requests.post(url, headers=headers, json=data)
        # Return the response text
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    
    except FileNotFoundError:
        return f"Error: Image file not found at path: {image_path}"
    except Exception as e:
        return f"An error occurred during analysis: {e}"  

def get_receipt_data(text):
    try: 
        return ast.literal_eval(text)
    except :
        print('Error converting the response fo')

