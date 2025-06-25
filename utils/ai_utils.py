import ast
import google.generativeai as genai
from PIL import Image as PILImage


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
        # Load the Gemini Pro Vision model
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Load the image using PIL
        img = PILImage.open(image_path)

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
        response = model.generate_content([prompt, img])

        # Return the response text
        return response.text     

    except FileNotFoundError:
        return f"Error: Image file not found at path: {image_path}"
    except Exception as e:
        return f"An error occurred during analysis: {e}"  

def get_receipt_data(text):
    splitted_text = text.rsplit('\n')
    try: 
        data = ast.literal_eval(splitted_text[1])
    except :
        data = ast.literal_eval(splitted_text[0])

    return data
