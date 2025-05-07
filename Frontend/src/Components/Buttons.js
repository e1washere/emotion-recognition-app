import React, { useContext } from "react";
import "./Buttons.css";
import { MediaContext } from "../Context/MediaContext";

export default function Buttons() {
  const { handleMediaChange, isWebcamOn, startWebcam, stopWebcam } =
    useContext(MediaContext);

  return (
    <div className="button-container">
      {isWebcamOn ? (
        <button className="button-style" onClick={() => stopWebcam()}>
          Stop Webcam
        </button>
      ) : (
        <>
          <input
            type="file"
            id="mediaInput"
            accept="image/*,video/*"
            onChange={handleMediaChange}
            style={{ display: "none" }}
          ></input>
          <button
            className="button-style"
            onClick={() => {
              document.getElementById("mediaInput").click();
            }}
          >
            Upload Image/Video
          </button>
          <button className="button-style" onClick={() => startWebcam()}>
            Start Webcam
          </button>
        </>
      )}
    </div>
  );
}
