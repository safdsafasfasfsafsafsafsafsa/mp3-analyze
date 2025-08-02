import axios from "../../api/axios";
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export default function DetailPage() {
  const BASE_URL = "https://image.tmdb.org/t/p/original";

  const { movieId } = useParams();
  // console.log("movieId", movieId);

  const [movie, setMovie] = useState({});

  useEffect(() => {
    async function fetchData() {
      const request = await axios.get(`/movie/${movieId}`);
      // console.log("request", request);
      setMovie(request.data);
    }
    fetchData();
  }, [movieId]);

  if (!movie) return <div>loading...</div>;

  return (
    <section>
      <img
        className="modal__poster-img" // 클래스명 재활용해 css 상속받기
        src={`${BASE_URL}${movie.backdrop_path}`}
        alt="poster"
      />
    </section>
  );
}
