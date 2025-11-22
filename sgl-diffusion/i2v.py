import time
import os
import requests
from openai import OpenAI

client = OpenAI(api_key="sk-proj-1234567890", base_url="http://localhost:3000/v1")

image_url = "https://github.com/Wan-Video/Wan2.2/blob/990af50de458c19590c245151197326e208d7191/examples/i2v_input.JPG?raw=true"
local_image = "i2v_input.jpg"
output_video = "output.mp4"

with open(local_image, "wb") as f:
    f.write(requests.get(image_url).content)

try:
    with open(local_image, "rb") as img_file:
        video = client.videos.create(
            prompt="A cat surfing on the sea.",
            input_reference=img_file,  
            size="832x480",
            seconds=10,
            extra_body={"fps": 16, "num_frames": 125},
        )

    while True:
        video = client.videos.retrieve(video_id=video.id)
        if video.status == "completed":
            break
        if video.status == "failed":
            raise Exception("Video generation failed")
        time.sleep(2)

    response = client.videos.download_content(video_id=video.id)
    content = response.read() if hasattr(response, "read") else response

    with open(output_video, "wb") as f:
        f.write(content)

finally:
    if os.path.exists(local_image):
        os.remove(local_image)