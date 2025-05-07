import * as faceapi from "face-api.js";
import { clearCanvas } from "./canvasUtils";

const options = new faceapi.TinyFaceDetectorOptions();

export async function loadModels() {
  try {
    await faceapi.nets.tinyFaceDetector.loadFromUri("./models");
    console.log("Models loaded");
  } catch (e) {
    console.error("Failed to load models", e);
    throw e;
  }
}

export async function detectFaces(media) {
  const detections = await faceapi.detectAllFaces(media, options);
  return detections;
}

export function drawBoundingBoxes(
  canvas,
  detections,
  mediaSize,
  mediaIdRef,
  currentMediaId,
  emotions
) {
  clearCanvas(canvas);

  if (mediaIdRef.current !== currentMediaId) return;

  const resizedDetections = faceapi.resizeResults(detections, mediaSize);
  resizedDetections.forEach((detection, i) => {
    const detectionBox = detection.box;
    const boxOptions = {
      label: emotions[i],
      lineWidth: 2,
    };

    console.log(emotions[i]);
    const box = new faceapi.draw.DrawBox(detectionBox, boxOptions);
    box.draw(canvas);
  });
}
