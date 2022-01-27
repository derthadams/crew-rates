import React, { useState } from 'react';

import { useLocation } from "react-router-dom";

function Failure(props) {
    const state = useLocation();

    return (
        <div>
            <h1>Failure</h1>
            {Object.keys(state.state).map((key) =>
            <p key={key}><span>{key}: </span><span>{state.state[key]}</span></p>)}
        </div>
    )
}

export default Failure;