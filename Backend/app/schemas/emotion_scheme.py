from pydantic import BaseModel

class EmotionScheme(BaseModel):
    emotion: str
    confidence: float