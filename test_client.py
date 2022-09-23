from __future__ import print_function
import requests
import json
import cv2
import time
import argparse
import pickle
import codecs


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", required=True, default=5000, type=int,
                help="path to input dataset")
args = vars(ap.parse_args())

addr = 'http://{}:{}'.format('127.0.0.1', args['port'])
test_url = addr + '/api/recognize'
download_url = addr + '/api/downloadID'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

loaded = False
while not loaded:
    try:
        response = requests.post(download_url, data='req')
        known_persons = pickle.loads(codecs.decode(json.loads(response.text)['message'].encode(), "base64"))
        users = [*known_persons]
        print(users)
        loaded = True
    except Exception as e:
        pass

img = cv2.imread('test.jpg')
# encode image as jpeg
for i in range(10):
    t0 = time.time()
    _, img_encoded = cv2.imencode('.jpg', img)
    # send http request with image and receive response
    response = requests.post(test_url, data=img_encoded.tobytes(), headers=headers)
    print('{} msec'.format((time.time() - t0) * 1e3))
    # decode response
    (persons, uknowns_cnt) = pickle.loads(codecs.decode(json.loads(response.text)['message'].encode(), "base64"))
    print(persons)
f = 0
img = cv2.resize(img, (300, 300))
img = img[persons[f][2][0]:persons[f][2][2], persons[f][2][3]:persons[f][2][1]]
cv2.imshow(persons[f][0], img)
cv2.waitKey(10000)

# expected output: {u'message': u'image received. size=124x124'}
