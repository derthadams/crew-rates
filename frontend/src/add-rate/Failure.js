import React, { useState } from 'react';

import {Navigate, useLocation} from "react-router-dom";

function Failure(props) {
    const locationState = useLocation();
    if( !locationState.state?.fromForm) {
        return <Navigate to="/" replace state={{fromForm: true}}/>
    }

    return (
        <div className="failure-container">
            <h1 className="display-1">Oops!</h1>
            <h2 className="mt-3">Something went wrong on our end.<br/></h2>
                <p>Please try your request again later.</p>
            {/*{locationState.state.errors && Object.keys(locationState.state.errors).map((key) =>*/}
            {/*<p key={key}><span>{key}: </span><span>{locationState.state.errors[key]}</span></p>)}*/}
        </div>
    )
}

export default Failure;