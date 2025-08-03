import "../styles/Reset.css";
import "./Nav.css";

export default function Nav() {
  console.log("nav");

  return (
    <nav className="nav">
      <img
        src="/img/mp3-analyze.png"
        alt="mp3-analyze logo"
        className="nav__logo"
        onClick={() => window.location.reload()}
      />
    </nav>
  );
}
