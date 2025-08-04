import React, { useRef, useState, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FileContext } from "../../contexts/FileContext";
import axios from "../../api/axios";

import Submit from "../../components/Submit";
import requests from "../../api/requests";

import "../../styles/Reset.css";
import "../../styles/PageLayout.css";

export default function MainPage() {
  const navigate = useNavigate();
  const { file } = useContext(FileContext);

  useEffect(() => {
    if (!file) {
      navigate("/");
    }
    fetchData(file);
  }, [file]);

  const fetchData = async (newFile) => {
    const formData = new FormData();
    formData.append("file", newFile);

    try {
      const response = await axios.post("/analyze", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const resultData = response.data;

      navigate(`/analyze`, { state: { result: resultData } });
    } catch (error) {
      console.Console("Error", error);
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
