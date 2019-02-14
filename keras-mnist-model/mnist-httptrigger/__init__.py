import logging
from keras.models import model_from_json
import pickle
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    ##Loading the MNIST Model
    weights = pickle.load(open('.\modelfiles\Keras-Mnist_weights.pkl', 'rb'))
    json = pickle.load(open('.\modelfiles\Keras-Mnist_json.pkl', 'rb'))
    model = model_from_json(json)
    model.set_weights(weights)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
