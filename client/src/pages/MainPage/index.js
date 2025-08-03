import Submit from "../../components/Submit";
import requests from "../../api/requests";

import "../../styles/Reset.css";
import "../../styles/PageLayout.css";

export default function MainPage() {
  console.log("main");

  return (
    <section className="main-page centered">
      <h1 className="title-h1">Insert music file</h1>
      <h2 className="title-h2">mp3, wav etc</h2>
      <Submit />
    </section>
  );
}
