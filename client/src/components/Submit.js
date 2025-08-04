import React, { useRef, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { FileContext } from "../contexts/FileContext";
import "./Submit.css";

export default function Submit({ nav }) {
  const fileInputRef = useRef();
  const navigate = useNavigate();

  // const [file, setFile] = useState(null);
  const { file } = useContext(FileContext);
  const { setFile } = useContext(FileContext);

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleFileUpload = (e) => {
    setFile(e.target.files[0]);
    console.log(e.target.files[0]);
    navigate(`/${nav}`);
  };

  return (
    <div>
      <button onClick={handleButtonClick} className="btn">
        Submit
      </button>
      <input
        type="file"
        accept=".mp3. .wav, audio/*"
        ref={fileInputRef}
        onChange={handleFileUpload}
        style={{ display: "none" }}
      />
    </div>
  );
}
