import base64
from fastapi import FastAPI, Query
from typing import List
import numpy as np
from Get_Image import get_image_by_id
import cv2
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageRequest(BaseModel):
    messages: List[str]


@app.post("/get_images")
async def get_images(request: ImageRequest):
    print(request.messages)
    Dataset_Path = "Dataset"  # Update this path accordingly
    results = get_image_by_id(request.messages, Dataset_Path)

    # Convert images to base64 strings for JSON compatibility
    for result in results:
        for id_key, image_value in result.items():
            if isinstance(image_value, np.ndarray) and id_key != "ERROR" and id_key != "SUCCESS":
                image_value = cv2.imencode('.jpg', image_value)[1]
                image_value = base64.b64encode(image_value).decode('utf-8')
            result[id_key] = image_value

    return results


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
