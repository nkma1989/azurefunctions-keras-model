import logging
from keras.models import model_from_json
import pickle
import azure.functions as func
import numpy as np
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    ##Loading the MNIST Model
    weights = pickle.load(open(os.environ['ModelWeightsPath'], 'rb'))
    json = pickle.load(open(os.environ['ModelJSONPath'], 'rb'))
    model = model_from_json(json)
    model.set_weights(weights)
    #Checking for a JSON object in the request body
    try: 
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
             "Please pass an json object in the request body",
             status_code=400
        )
    #Checking for an image in the request body
    raw_data=req_body.get('image')
    #Processing image
    if raw_data:
        data = np.array(raw_data,np.uint8)
        prediction = model.predict(data)
        #Maximum probability prediction
        logging.info(np.argmax(prediction))
    else:
        return func.HttpResponse(
             "Please pass an image in the request body",
             status_code=400
        )

    return func.HttpResponse(f"{np.argmax(prediction)}")
