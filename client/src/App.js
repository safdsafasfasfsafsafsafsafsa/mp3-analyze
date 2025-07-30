import React, { useState, useEffect } from "react";
import "./App.css";

export default function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("/members");
        const result = await res.json();
        setData(result.members);
        console.log("result.members", result.members);
      } catch (error) {
        console.error("error", error);
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Members</h1>
      <ul>
        {data.map((member, index) => (
          <li key={index}>{member}</li>
        ))}
      </ul>
    </div>
  );
}
