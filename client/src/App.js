import React, { useState, useEffect } from "react";
import "./App.css";

export default function App() {
  const API_BASE = process.env.REACT_APP_API_BASE;

  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      // try {
      //   const res = await fetch("/members");
      //   const result = await res.json();
      //   setData(result.members);
      //   console.log("result.members", result.members);
      // } catch (error) {
      //   console.error("error", error);
      // }
      try {
        const res = await fetch(`${API_BASE}/`);
        const result = await res.json();
        setData(result);
        console.log("Result:", result);
      } catch (error) {
        console.error("Error:", error);
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Members</h1>
      <ul>
        {data.members &&
          data.members.map((member, index) => <li key={index}>{member}</li>)}
      </ul>
    </div>
  );
}
