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
      <p className="analyze-page__result">파일 이름: {file.name}</p>
      <p className="analyze-page__result">파일 크기: {file.size}</p>
      <p className="analyze-page__result">BPM: {result.bpm}</p>
      <p className="analyze-page__result">길이: {result.duration}</p>
      <p className="analyze-page__result">리듬 밀도: {result.rhythm_density}</p>
      <p className="analyze-page__result">
        크레스트 팩터(Peak/RMS): {result.crest_factor}
      </p>
      <p className="analyze-page__result">믹싱: {result.mixing_type}</p>
      {result.image && (
        <img
          className="analyze-page__result"
          src={`data:image/png;base64,${result.image}`}
          alt="분석 그래프"
        />
      )}
    </section>
  ) : (
    <section className="analyze-page centered">nnn</section>
  );
}
