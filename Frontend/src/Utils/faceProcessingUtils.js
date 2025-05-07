import { drawBoundingBoxes } from "./faceDetectionUtils";

export async function cropFaces(
  detections,
  mediaElement,
  selectedModel,
  canvas,
  mediaSize,
  mediaIdRef,
  currentMediaId
) {
  const emotions = [];

  for (let detection of detections) {
    const { x, y, width: boxWidth, height: boxHeight } = detection.box;

    const faceCanvas = document.createElement("canvas");
    faceCanvas.width = boxWidth;
    faceCanvas.height = boxHeight;
    const faceCanvasContext = faceCanvas.getContext("2d");

    faceCanvasContext.drawImage(
      mediaElement,
      x,
      y,
      boxWidth,
      boxHeight,
      0,
      0,
      boxWidth,
      boxHeight
    );

    const faceDataUrl = faceCanvas.toDataURL("image/jpeg");
    const emotion = await detectEmotion(faceDataUrl, selectedModel);

    emotions.push(emotion);
  }

  drawBoundingBoxes(
    canvas,
    detections,
    mediaSize,
    mediaIdRef,
    currentMediaId,
    emotions
  );
}

async function detectEmotion(faceDataUrl, selectedModel) {
  try {
    const base64Image = faceDataUrl.split(",")[1];

    const parameters = {
      image_data: base64Image,
      model_name: selectedModel,
    };

    const response = await fetch("http://127.0.0.1:8000/api/predict_emotion", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(parameters),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    const { emotion } = data;

    return emotion;
  } catch (e) {
    console.error("Error processing cropped face:", e);
    return null;
  }
}
