import "./Display.css";
import Webcam from "react-webcam";
import { useContext, useEffect, useRef } from "react";
import { clearCanvasRef } from "../Utils/canvasUtils";
import { runDetection } from "../Utils/displayUtils";
import { MediaContext } from "../Context/MediaContext";

export default function Display() {
  const { media, mediaType, isWebcamOn, selectedModel } =
    useContext(MediaContext);

  const canvasRef = useRef(null);
  const mediaRef = useRef(null);
  const webcamRef = useRef(null);
  const animationFrameRef = useRef(null);
  const mediaIdRef = useRef(0);

  useEffect(() => {
    clearCanvasRef(canvasRef);

    const mediaElement = isWebcamOn
      ? webcamRef.current.video
      : mediaRef.current;

    mediaIdRef.current += 1;
    const currentMediaId = mediaIdRef.current;

    if (!mediaElement) return;

    runDetection(
      mediaType,
      mediaElement,
      mediaIdRef,
      currentMediaId,
      canvasRef,
      animationFrameRef,
      selectedModel
    );
  }, [media, mediaType, isWebcamOn, selectedModel]);

  return (
    <div className="display-container">
      {isWebcamOn ? (
        <Webcam
          className="webcam"
          videoConstraints={{
            width: 800,
            height: 450,
          }}
          ref={webcamRef}
        />
      ) : media ? (
        mediaType === "image" ? (
          <img src={media} className="media" ref={mediaRef} alt="Image"></img>
        ) : (
          <video
            controls
            autoPlay
            muted
            loop
            src={media}
            className="media"
            ref={mediaRef}
          ></video>
        )
      ) : (
        <p className="text">No media selected</p>
      )}
      <canvas ref={canvasRef} className="canvasStyle" />
    </div>
  );
}
