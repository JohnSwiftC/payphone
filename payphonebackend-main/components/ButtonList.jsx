import React from 'react';
import Button from './Button';


const ButtonList = (props) => {

    return (
        <ul>
            {props.funcs.map((func) => <Button func={func}/>)}
        </ul>
    )
}

export default ButtonList;