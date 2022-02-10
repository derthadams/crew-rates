import React, { useState, useEffect } from "react";
import ReportContainer from "./ReportContainer";
import axios from "axios";

export default function App() {
    const [reports, setReports] = useState([]);
    const genre = JSON.parse(
        document.getElementById("genre").textContent
    );
    const unionStatus = JSON.parse(
        document.getElementById("unionStatus").textContent
    );
    console.log(unionStatus)
    const apiUrls = JSON.parse(document.getElementById("apiUrls").textContent);

    const getInitialData = () => {
        axios.get(apiUrls["rate-report-list"]).then((response) => {
            const initialData = response.data;
            console.log(initialData);
            setReports(initialData);
        });
    };

    useEffect(() => {
        getInitialData();
    }, []);

    return (
        <div className="my-3">
            <h1 className={"display-1"}>Discover</h1>
            <ReportContainer reports={reports}
                             genre={genre}
                             unionStatus={unionStatus} />
        </div>
    );
}
