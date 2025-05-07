export const clearCanvas = (canvas) => {
  const context = canvas.getContext("2d");
  context.clearRect(0, 0, canvas.width, canvas.height);
};

export const clearCanvasRef = (canvasRef) => {
  const canvas = canvasRef.current;
  const context = canvas.getContext("2d");
  context.clearRect(0, 0, canvas.width, canvas.height);
};

export const createCanvas = (mediaElement, canvasRef) => {
  const canvas = canvasRef.current;
  const mediaRect = mediaElement.getBoundingClientRect();

  const width = mediaRect.width;
  const height = mediaRect.height;
  canvas.width = width;
  canvas.height = height;

  const mediaSize = { width: width, height: height };

  return { canvas, mediaSize };
};
