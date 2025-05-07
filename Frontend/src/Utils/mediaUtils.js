import { useState } from "react";

export default function MediaUtils() {
  const [media, setMedia] = useState(null);
  const [mediaType, setMediaType] = useState(null);
  const [isWebcamOn, setIsWebcamOn] = useState(false);
  const [selectedModel, setSelectedModel] = useState("fer2013_pytorch");
  const models = [
    "fer2013_pytorch",
    "fer2013_tf",
    "kdef_pytorch",
    "kdef_tf",
    "mixed_pytorch",
    "mixed_tf",
    "nhfi_pytorch",
    "nhfi_tf",
  ];

  const VALID_TYPES = ["image/", "video/"];

  const handleMediaChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!VALID_TYPES.some((type) => file.type.startsWith(type))) {
      console.error("Error set: Invalid file type");
      return;
    }

    if (file) {
      setMedia(URL.createObjectURL(file));
      if (file.type.startsWith("image")) {
        setMediaType("image");
      } else if (file.type.startsWith("video")) {
        setMediaType("video");
      }
    }
  };

  const startWebcam = () => {
    if (media) {
      setMedia(null);
      setMediaType(null);
    }

    setIsWebcamOn(true);
  };

  const stopWebcam = () => {
    setIsWebcamOn(false);
  };

  return {
    media,
    mediaType,
    isWebcamOn,
    handleMediaChange,
    startWebcam,
    stopWebcam,
    selectedModel,
    setSelectedModel,
    models,
  };
}
