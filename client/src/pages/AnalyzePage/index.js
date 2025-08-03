import axios from "../../api/axios";
import React, { useEffect, useState, useContext } from "react";
import { useParams } from "react-router-dom";
import { FileContext } from "../../contexts/FileContext";

import "../../styles/Reset.css";
import "../../styles/PageLayout.css";

export default function AnalyzePage() {
  console.log("analyze");

  const { file } = useContext(FileContext);

  return file ? (
    <section className="analyze-page centered">aaa</section>
  ) : (
    <section className="analyze-page centered">nnn</section>
  );
}
