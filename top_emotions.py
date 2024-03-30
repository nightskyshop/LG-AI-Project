from hume import HumeBatchClient
from hume.models.config import ProsodyConfig
import math

client = HumeBatchClient('tRneADQIiTqoaD8m42PUTKWtD8e4zRte4n6JP3f0gaCgT6XC')
urls = ['https://gohistory.pythonanywhere.com/media/audios/%EA%B3%A0%EB%8C%80_38%EC%9E%A5_%EC%9D%B4%EC%9D%B8%ED%98%9C.mp3']
prosody_config = ProsodyConfig()

job = client.submit_job(urls, [prosody_config])
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