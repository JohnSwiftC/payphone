import React from 'react';
import style from './stylemod.module.css';
import { respondMessageUpdateContext } from '../App'

import { useContext } from 'react';

const Button = (props) => {

    const func = props.func;

    const setMOTD = useContext(respondMessageUpdateContext);

    const onClick = async () => {
        const response = await fetch("http://localhost:8000/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({"func" : func})
          })

        const message = await response.json();
        setMOTD(message.data);
    }

    return (
        <button className={style.button} onClick={() => onClick()}>
            <span>{func}</span>
        </button>
    )
}

export default Button;