import logo from "./logo.svg";
import Header from "./components/Header";
import ButtonList from "./components/ButtonList";
import "./App.css";

import style from "./components/stylemod.module.css";

import { createContext, useState, useEffect } from "react";

export const respondMessageUpdateContext = createContext();

function App() {
  document.body.style = "background: green;";

  const [funcs, setFuncs] = useState([]);
  const [gifLink, setGifLink] = useState("");
  const [motd, setMOTD] = useState("Welcome!");

  const fetchActs = async () => {
    const response = await fetch("http://localhost:8000/");
    const acts = await response.json();
    setFuncs(acts.data);
  };

  const fetchGif = async () => {
    const response = await fetch("http://localhost:8000/gif");
    const gif = await response.json();
    setGifLink(gif.data);
  };

  useEffect(() => {
    fetchActs();
    fetchGif();
  }, []);

  document.body.style = "background: green;";

  return (
    <>
      <Header />
      <div className={style.row}>
        <div className={style.column}>
          <respondMessageUpdateContext.Provider value={setMOTD}>
            <ButtonList funcs={funcs} />
          </respondMessageUpdateContext.Provider>
        </div>
        <div className={style.columnRight}>
          <p style={{ fontSize: 30 }}>Daddy says: {motd}</p>
          <br></br>
          <iframe
            src={gifLink}
            width="480"
            height="326"
            class="giphy-embed"
          ></iframe>
          <br></br>
          <button className={style.button} onClick={() => fetchGif()}>
            Change GIF
          </button>
        </div>
      </div>
    </>
  );
}

export default App;
