import io
import base64

import numpy as np

import matplotlib.pyplot as plt

data = {
    "Anger": 18.6,
    "Disgust": 13.3,
    "Fear": 11.4,
    "Joy": 33.6,
    "Sadness": 8.0,
    "Surprise": 23.1
}

label_loc = np.linspace(start=0, stop=2*np.pi-1, num=len(data.keys()))

fig, ax = plt.subplots(1,1, figsize=(5,20), subplot_kw={'projection': 'polar'})
ax.set_xticks(label_loc, labels=data.keys(), fontsize=13)
ax.plot(label_loc, data.values(), color="skyblue")
ax.fill(label_loc, data.values(), color="skyblue", alpha=0.3)

my_stringIObytes = io.BytesIO()
plt.savefig(my_stringIObytes, format='jpg', bbox_inches="tight")
my_stringIObytes.seek(0)
my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
print(my_base64_jpgData)