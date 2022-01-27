import React from 'react';

import { BrowserRouter, Routes, Route } from "react-router-dom";

import { StateMachineProvider, createStore } from "little-state-machine";
import { DevTool } from 'little-state-machine-devtools';

import PageOne from "./PageOne"
import PageTwo from "./PageTwo"
import PageThree from "./PageThree"
import Success from "./Success"
import Failure from "./Failure"

const BASE_URL = 'https://localhost:8000/api/';

createStore({
    locationDetails: {},
    formData: {
        show_title: '',
        season_number: '',
        companies: [],
        network: '',
        genre: '',
        union: '',
        locations: [],
        start_date: '',
        end_date: '',
        job_title: '',
        offered_guarantee: '',
        offered_day_rate: '',
        offered_hourly_rate: '',
        negotiated: '',
        increased: '',
        final_guarantee: '',
        final_day_rate: '',
        final_hourly_rate: '',
    }
}, {});

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
export { BASE_URL };