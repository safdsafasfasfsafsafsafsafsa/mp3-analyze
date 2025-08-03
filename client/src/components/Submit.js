import React, { useRef, useState } from "react";
import axios from "../api/axios";
import "./Submit.css";

export default function Submit() {
  const fileInputRef = useRef();
  const [file, setFile] = useState(null);

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleFileUpload = (e) => {
    setFile(e.target.files[0]);
    console.log(e.target.files[0]);
  };

  // const HandleSubmit = async () => {
  //   if (!file) {
  //     alert("파일 선택");
  //     return;
  //   }
  // };

  return (
    <div>
      <button onClick={handleButtonClick} className="btn">
        Submit
      </button>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileUpload}
        style={{ display: "none" }}
      />
    </div>
  );
}
