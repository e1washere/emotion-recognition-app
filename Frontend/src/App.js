import "./App.css";
import { useEffect, useState } from "react";
import Display from "./Components/Display";
import Buttons from "./Components/Buttons";
import ModelPicker from "./Components/ModelPicker";
import { MediaProvider } from "./Context/MediaContext";
import { loadModels } from "./Utils/faceDetectionUtils";

function App() {
  const [isModelLoaded, setIsModelLoaded] = useState(false);

  useEffect(() => {
    loadModels()
      .then(() => {
        setIsModelLoaded(true);
      })
      .catch(() => {
        console.error("Failed to load models");
      });
  }, []);

  if (!isModelLoaded) {
    return (
      <div className="app-container">
        <h2>Loading face models...</h2>
      </div>
    );
  }

  return (
    <MediaProvider>
      <div className="app-container">
        <Display />
        <ModelPicker />
        <Buttons />
      </div>
    </MediaProvider>
  );
}

export default App;
