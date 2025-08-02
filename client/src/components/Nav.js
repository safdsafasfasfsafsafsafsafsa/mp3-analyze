import "./Nav.css";

export default function Nav() {
  return (
    <nav className="nav">
      <img
        src="../../public/img/mp3-analyze.png"
        alt="mp3-analyze logo"
        className="nav__logo"
        onClick={() => window.location.reload()}
      />
    </nav>
  );
}
