# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 13:18:08 2019

@author: NielsKristianAnderse
"""

import requests
import glob
import cv2
import os
import json
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='This scripts is used test the function API')
parser.add_argument(
    '-e',
    '--endpoint',
    type=str,
    required=True,
    help='Endpoint of the function API')

def _main_(args):
    
    #API definition
    endpoint=args.endpoint
    
    print(f"Using endpoint: {args.endpoint}")
    print('-------------------------------------------------------------')
    
    headers = {'Content-Type':'application/json'}
    paths=glob.glob(r'.\testimages\*.jpg')
    for image in paths:
        print(image)
        img=cv2.imread(image,cv2.IMREAD_GRAYSCALE)
        img=np.reshape(img,(1,28,28,1))
        test_sample = json.dumps({"image": img.tolist()})
        resp = requests.post(endpoint, test_sample, headers=headers)
        print(f"input shape: {img.shape}")
        print(f"label {os.path.basename(image).split('.jpg')[0]}")
        print(f"prediction {resp.text}")
        print('-------------------------------------------------------------')


if __name__ == "__main__":
    args = parser.parse_args()
    _main_(args)
    