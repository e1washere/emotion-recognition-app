import { createCanvas } from "./canvasUtils";
import { detectFaces } from "./faceDetectionUtils";
import { cropFaces } from "./faceProcessingUtils";

const DETECTION_INTERVAL = 500;
let lastDetectionTime = 0;
const detectAndDraw = async (
  mediaElement,
  canvas,
  mediaSize,
  mediaIdRef,
  currentMediaId,
  selectedModel
) => {
  const detections = await detectFaces(mediaElement);

  await cropFaces(
    detections,
    mediaElement,
    selectedModel,
    canvas,
    mediaSize,
    mediaIdRef,
    currentMediaId
  );
};

const handleLoad = async (
  mediaElement,
  mediaIdRef,
  currentMediaId,
  canvasRef,
  selectedModel
) => {
  const { canvas, mediaSize } = createCanvas(mediaElement, canvasRef);

  await detectAndDraw(
    mediaElement,
    canvas,
    mediaSize,
    mediaIdRef,
    currentMediaId,
    selectedModel
  );
};

const frameLoop = (
  mediaElement,
  canvas,
  mediaSize,
  mediaIdRef,
  currentMediaId,
  animationFrameRef,
  selectedModel
) => {
  animationFrameRef.current = requestAnimationFrame(async (timestamp) => {
    try {
      if (
        timestamp - lastDetectionTime >= DETECTION_INTERVAL &&
        mediaElement.readyState >= 2 &&
        !mediaElement.paused &&
        !mediaElement.ended
      ) {
        lastDetectionTime = timestamp;

        await detectAndDraw(
          mediaElement,
          canvas,
          mediaSize,
          mediaIdRef,
          currentMediaId,
          selectedModel
        );
      }
    } catch (error) {
      console.error("Error in detection loop:", error);
    }

    frameLoop(
      mediaElement,
      canvas,
      mediaSize,
      mediaIdRef,
      currentMediaId,
      animationFrameRef,
      selectedModel
    );
  });
};

const onLoadedData = (
  mediaElement,
  mediaIdRef,
  currentMediaId,
  canvasRef,
  animationFrameRef,
  selectedModel
) => {
  const { canvas, mediaSize } = createCanvas(mediaElement, canvasRef);

  lastDetectionTime = 0;

  if (animationFrameRef.current) {
    cancelAnimationFrame(animationFrameRef.current);
  }

  frameLoop(
    mediaElement,
    canvas,
    mediaSize,
    mediaIdRef,
    currentMediaId,
    animationFrameRef,
    selectedModel
  );
};

export const runDetection = (
  mediaType,
  mediaElement,
  mediaIdRef,
  currentMediaId,
  canvasRef,
  animationFrameRef,
  selectedModel
) => {
  if (mediaType === "image") {
    mediaElement.onload = () =>
      handleLoad(
        mediaElement,
        mediaIdRef,
        currentMediaId,
        canvasRef,
        selectedModel
      );

    if (mediaElement.complete) {
      handleLoad(
        mediaElement,
        mediaIdRef,
        currentMediaId,
        canvasRef,
        selectedModel
      );
    }

    return () => {
      mediaElement.onload = null;
    };
  } else {
    mediaElement.onloadeddata = () =>
      onLoadedData(
        mediaElement,
        mediaIdRef,
        currentMediaId,
        canvasRef,
        animationFrameRef,
        selectedModel
      );

    if (
      mediaElement.readyState >= 2 &&
      !mediaElement.paused &&
      !mediaElement.ended
    ) {
      onLoadedData(
        mediaElement,
        mediaIdRef,
        currentMediaId,
        canvasRef,
        animationFrameRef,
        selectedModel
      );
    }

    return () => {
      mediaElement.onloadeddata = null;
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }
};
