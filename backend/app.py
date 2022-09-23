from flask import Flask, request, Response, render_template
import jsonpickle
import numpy as np
import cv2
from face_rec import face_rec as fr
import argparse
import pickle
import logging
import codecs


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", required=True, default=5000, type=int,
                help="path to input dataset")
args = vars(ap.parse_args())

logger = logging.getLogger('recognition_thread_at_port_' + str(args['port']))
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('Logs/log_recognition_thread_at_port_' + str(args['port']) + '.txt')
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

recognizer = fr.FaceRecognizer(logger)


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/api/recognize', methods=['POST'])
def recognize_request():
    recogn = recognizer
    r = request
    nparr = np.frombuffer(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    persons = []
    msg = codecs.encode(pickle.dumps(persons), "base64").decode()
    (res, persons, unknowns_cnt) = recogn.recognize_face(img)
    if res:
        msg = codecs.encode(pickle.dumps((persons, unknowns_cnt)), "base64").decode()
    response = {'message': msg}

    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/api/downloadID', methods=['POST'])
def download_request():
    r = request
    recogn = recognizer
    msg = codecs.encode(pickle.dumps(recogn.known_persons), "base64").decode()
    response = {'message': msg}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
