from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        # Connect to the "reviews" database
        db = client["reviews"]
        
        # Create a new review document
        review = {
            "name": "John Doe",
            "review": "Great service!",
            "rating": 5
        }
        
        # Save the review document to the database
        db.create_document(review)
        
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"result": "Review posted successfully"}