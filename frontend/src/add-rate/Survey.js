import React from 'react';

import { BrowserRouter, Routes, Route } from "react-router-dom";

import { StateMachineProvider, createStore } from "little-state-machine";
import { DevTool } from 'little-state-machine-devtools';

import PageOne from "./PageOne"
import PageTwo from "./PageTwo"
import PageThree from "./PageThree"
import Success from "./Success"
import Failure from "./Failure"

import { dataDefault } from "./dataDefault"

createStore(dataDefault, {});

function Survey() {
    return (
        <StateMachineProvider>
            {process.env.NODE_ENV !== 'production' && <DevTool/>}
            <BrowserRouter basename="/add-rate">
                <Routes>
                    <Route path="/" element={<PageOne/>} />
                    <Route path="/2" element={<PageTwo/>} />
                    <Route path="/3" element={<PageThree/>}/>
                    <Route path="/success" element={<Success/>}/>
                    <Route path="/404" element={<Failure/>}/>
                </Routes>
            </BrowserRouter>
        </StateMachineProvider>
    );
}

export default Survey;