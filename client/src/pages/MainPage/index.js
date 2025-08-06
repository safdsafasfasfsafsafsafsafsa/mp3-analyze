import React, { useRef, useState, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FileContext } from "../../contexts/FileContext";

import axios from "../../api/axios";
import requests from "../../api/requests";
import Submit from "../../components/Submit";

import "../../styles/Reset.css";
import "../../styles/PageLayout.css";

export default function MainPage() {
  const navigate = useNavigate();
  const { file } = useContext(FileContext);

  useEffect(() => {
    if (file) {
      console.log("file here");
      console.log(file);
      console.log(typeof file);
      console.log(file instanceof File); // true 여야 제대로 작동
      fetchData(file);
    }
  }, [file]);

  const fetchData = async (newFile) => {
    const formData = new FormData();
    formData.append("file", newFile);

    try {
      console.log("loading...1");

      const response = await axios.post("/analyze", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log(response.data);
      console.log("loading...2");

      const resultData = response.data;

      navigate(`/analyze`, { state: { result: resultData } });
    } catch (error) {
      console.error("Error", error);
      console.error("upload error", error.response?.data || error.message);
    }
  };

  return (
    <section className="main-page centered">
      <h1 className="title-h1">Insert music file</h1>
      <h2 className="title-h2">mp3, wav etc</h2>
      <Submit nav="analyze" />
    </section>
  );
}
