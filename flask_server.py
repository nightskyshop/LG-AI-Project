from flask import Flask, request

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import firestore as google_firestore

from hume import HumeBatchClient
from hume.models.config import ProsodyConfig
from hume._batch.transcription_config import TranscriptionConfig


from pytz import timezone
from dotenv import load_dotenv
import os
import datetime
import time

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

collection_name = "emotions"

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = HumeBatchClient(API_KEY)
transcription_config = TranscriptionConfig(language="ko")
prosody_config = ProsodyConfig()

app = Flask(__name__)

@app.route("/", methods=["POST"])
def create_emotion():
    url = request.get_json()["url"]

    urls = [url]

    job = client.submit_job(urls, [prosody_config], transcription_config)
    print(job)
    print('Running...')

    start = time.time()

    job.await_complete()
    job_predictions = client.get_job_predictions(job_id=job.id)

    print("midtime :", time.time() - start)

    emotions_dict = dict()

    for file in job_predictions:
        for prediction in file['results']['predictions']:
            for grouped_prediction in prediction['models']['prosody']['grouped_predictions']:
                for grouped_prediction_prediction in grouped_prediction['predictions']:
                    for emotion in grouped_prediction_prediction['emotions']:
                        if emotion['name'] == "Joy" or emotion['name'] == "Anger" or emotion['name'] == "Fear" or emotion['name'] == "Sadness" or emotion['name'] == "Disgust" or emotion['name'] == "Surprise":
                            if emotion['name'] not in emotions_dict:
                                emotions_dict[emotion['name']] = emotion['score']
                            else:
                                emotions_dict[emotion['name']] = emotions_dict[emotion['name']] + emotion['score']

    emotions_average = dict()

    total = 0

    for _, score in emotions_dict.items():
        total += score

    for emotion, score in emotions_dict.items():
        emotions_average[emotion] = round((score / total) * 100, 1)
    
    ascend_sorted_emotion_average = sorted(emotions_average, key=emotions_average.get, reverse=True)

    emotion_last = 100

    for i in range(4):
        emotion_last -= emotions_average[ascend_sorted_emotion_average[i]]
    
    emotions_average[ascend_sorted_emotion_average[-1]] = emotion_last

    emotions_average["audio"] = url
    emotions_average["createdAt"] = datetime.datetime.now(timezone("Asia/Seoul"))

    doc_ref = db.collection(collection_name).document()
    doc_ref.set(emotions_average)

    print("endtime :", time.time() - start)

    return emotions_average

if __name__ == "__main__":
		app.run()