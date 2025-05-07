from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.model_loader import get_model
from app.utils.emotions_7 import get_emotion_label_7
from app.utils.emotions_8 import get_emotion_label_8
from app.schemas.emotion_scheme import EmotionScheme
from PIL import Image, UnidentifiedImageError
import base64
from io import BytesIO
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()

executor = ThreadPoolExecutor()

class ImagePayload(BaseModel):
    image_data: str
    model_name: str

@router.post("/predict_emotion", response_model=EmotionScheme)
async def predict_emotion_endpoint(payload: ImagePayload):
    try:
        image_data = payload.image_data
        model_name = payload.model_name

        imageb64 = base64.b64decode(image_data)
        image = Image.open(BytesIO(imageb64))

    except (UnidentifiedImageError, base64.binascii.Error):
        raise HTTPException(status_code=400, detail="Invalid image data.")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

    try:
        model = get_model(model_name)
        preprocessed_image = model.preprocess(image)

        loop = asyncio.get_event_loop()
        predicted_class, confidence = await loop.run_in_executor(
            executor, model.predict, preprocessed_image
        )

        if model_name not in ['nhfi_pytorch', 'nhfi_tf']:
            emotion = get_emotion_label_7(predicted_class)
        else:
            emotion = get_emotion_label_8(predicted_class)

        return EmotionScheme(emotion=emotion, confidence=confidence)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")
