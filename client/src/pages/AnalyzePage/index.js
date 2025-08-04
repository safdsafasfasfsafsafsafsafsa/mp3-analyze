import axios from "../../api/axios";
import React, { useEffect, useState, useContext } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { FileContext } from "../../contexts/FileContext";

import "../../styles/Reset.css";
import "../../styles/PageLayout.css";

export default function AnalyzePage() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;

  const { file } = useContext(FileContext);

  useEffect(() => {
    if (!result) {
      navigate(`/`);
    }
  }, [result, navigate]);
  if (!result) return null;

  return file ? (
    <section className="analyze-page centered">
      <p>{file.bpm}</p>
    </section>
  ) : (
    <section className="analyze-page centered">nnn</section>
  );
}
