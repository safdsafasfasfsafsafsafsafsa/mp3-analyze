// import React, { useState, useEffect } from "react";
import Nav from "./components/Nav";
import Footer from "./components/Footer";
import MainPage from "./pages/MainPage/index";
import AnalyzePage from "./pages/AnalyzePage/index";
import { Outlet, Routes, Route } from "react-router-dom";
import "./App.css";

const Layout = () => {
  return (
    <div>
      <Nav />
      <Outlet />
      <Footer />
    </div>
  );
};

export default function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<MainPage />}></Route>
          <Route path="analyze" element={<AnalyzePage />}></Route>
        </Route>
      </Routes>
    </div>
  );
}

// export default function App() {
//   const API_BASE = process.env.REACT_APP_API_BASE;

//   const [data, setData] = useState([]);

//   useEffect(() => {
//     const fetchData = async () => {
//       try {
//         const res = await fetch(`${API_BASE}/`);
//         const result = await res.json();
//         setData(result);
//         console.log("Result:", result);
//       } catch (error) {
//         console.error("Error:", error);
//       }
//     };
//     fetchData();
//   }, []);

//   return (
//     <div>
//       <h1>Members</h1>
//       <ul>
//         {data.members &&
//           data.members.map((member, index) => <li key={index}>{member}</li>)}
//       </ul>
//     </div>
//   );
// }
