import logging
from keras.models import model_from_json
import pickle
import azure.functions as func
import numpy as np
import os
import cv2
from azure.cosmosdb.table.tableservice import TableService
import re
import datetime

def main(myblob: func.InputStream, outputblob: func.Out[func.InputStream]):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    ##Loading the MNIST Model
    weights = pickle.load(open(os.environ['ModelWeightsPath'], 'rb'))
    json = pickle.load(open(os.environ['ModelJSONPath'], 'rb'))
    model = model_from_json(json)
    model.set_weights(weights)
    #Reading image stream
    imgStream=myblob.read(-1)
    #Converting to image object
    nparr = np.fromstring(imgStream, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    img=img.reshape(1,28,28,1)
    logging.info(img.shape)
    #Predicting on image
    prediction = model.predict(img)
    #Maximum probability prediction
    logging.info(np.argmax(prediction))
    #Connection to table storage
    table_service = TableService(connection_string=os.environ['AzureWebJobsStorage'])
    #Storing in table storage (adding 1 hour to convert servertime to my timezone)
    values=[os.path.basename(myblob.name),str(datetime.datetime.now()+datetime.timedelta(hours=1)),str(np.argmax(prediction))]
    names=["PartitionKey","RowKey","Prediction"]
    dictionary = dict(zip(names, values))
    table_service.insert_entity('imagedata', dictionary)

    #Saving to output container - Shows how to save a possible processed image
    outputblob.set(imgStream)
