from hume import HumeBatchClient
from hume.models.config import ProsodyConfig
import time

start = time.time()

client = HumeBatchClient("tRneADQIiTqoaD8m42PUTKWtD8e4zRte4n6JP3f0gaCgT6XC")
urls = ["https://gohistory.pythonanywhere.com/media/audios/%EA%B3%A0%EB%8C%80_38%EC%9E%A5_%EC%9D%B4%EC%9D%B8%ED%98%9C.mp3"]
configs = [ProsodyConfig()]
job = client.submit_job(urls, configs)

print(job)
print("Running...")

job.await_complete()
predictions = job.get_predictions()
print(predictions)

print(time.time() - start)