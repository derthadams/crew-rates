import React, { useState } from 'react';

import {Navigate, useLocation} from "react-router-dom";

function Failure(props) {
    const locationState = useLocation();
    if( !locationState.state?.fromForm) {
        return <Navigate to="/" replace state={{fromForm: true}}/>
    }

    return (
        <div>
            <h1>Failure</h1>
            {locationState.state.errors && Object.keys(locationState.state.errors).map((key) =>
            <p key={key}><span>{key}: </span><span>{locationState.state.errors[key]}</span></p>)}
        </div>
    )
}

export default Failure;