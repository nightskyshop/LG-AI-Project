from hume import HumeBatchClient
from hume.models.config import ProsodyConfig
from hume._batch.transcription_config import TranscriptionConfig

import math


client = HumeBatchClient('tRneADQIiTqoaD8m42PUTKWtD8e4zRte4n6JP3f0gaCgT6XC')
urls = ['https://firebasestorage.googleapis.com/v0/b/uuuuu-bbd69.appspot.com/o/audio%2F%E1%84%90%E1%85%A6%E1%84%89%E1%85%B3%E1%84%90%E1%85%B3%20%E1%84%8B%E1%85%A9%E1%84%83%E1%85%B5%E1%84%8B%E1%85%A9.mp3?alt=media&token=59144b74-bf22-4fd5-9fe7-dcba20f65b28']
prosody_config = ProsodyConfig()
transcription_config = TranscriptionConfig(language="ko")

job = client.submit_job(urls, configs=[prosody_config], transcription_config=transcription_config)
print(job)
print('Running...')

result = job.await_complete()
job_predictions = client.get_job_predictions(job_id=job.id)

# The start and end time range of predictions to be processed
start_time = 0
end_time = math.ceil(job_predictions[0]['results']['predictions'][0]['models']['prosody']['grouped_predictions'][0]['predictions'][-1]['time']['end'])

# Top n emotions
n_top_values = 5

emotions_dict = dict()

# This for facial expressions. This can be modified for other models
for file in job_predictions:
    for prediction in file['results']['predictions']:
        for grouped_prediction in prediction['models']['prosody']['grouped_predictions']:
            for grouped_prediction_prediction in grouped_prediction['predictions']:
                if grouped_prediction_prediction['time']['begin'] >= start_time and grouped_prediction_prediction['time']['end'] <= end_time:
                    for emotion in grouped_prediction_prediction['emotions']:
                        if emotion['name'] == "Joy" or emotion['name'] == "Anger" or emotion['name'] == "Fear" or emotion['name'] == "Sadness" or emotion['name'] == "Disgust" or emotion['name'] == "Surprise":
                            if emotion['name'] not in emotions_dict:
                                emotions_dict[emotion['name']] = emotion['score']
                            else:
                                emotions_dict[emotion['name']] = emotions_dict[emotion['name']] + emotion['score']

emotions_average = dict()
emotion_dict_length = len(emotions_dict)

for emotion, score in emotions_dict.items():
    emotions_average[emotion] = score / emotion_dict_length

print(emotions_average)

ascend_sorted_emotion_average = sorted(emotions_average, key=emotions_average.get, reverse=True)

print ('The top {} expressed emotions are between timestamp {} and {} : '.format(n_top_values, start_time, end_time))

for i in range(0,n_top_values):
    print(ascend_sorted_emotion_average[i])