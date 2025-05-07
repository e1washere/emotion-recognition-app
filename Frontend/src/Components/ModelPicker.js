import React, { useContext } from "react";
import "./ModelPicker.css";
import { MediaContext } from "../Context/MediaContext";

export default function ModelPicker() {
  const { selectedModel, setSelectedModel, models } = useContext(MediaContext);
  return (
    <div className="modelPickerContainer">
      <label htmlFor="model-select">Select model:</label>
      <select
        id="model-select"
        value={selectedModel}
        onChange={(e) => setSelectedModel(e.target.value)}
      >
        {models.map((model) => (
          <option key={model} value={model}>
            {model}
          </option>
        ))}
      </select>
    </div>
  );
}
