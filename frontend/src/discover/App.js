import React, { useState, useEffect } from "react";
import RateReport from "./RateReport";
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
            <h6 className={"display-6"}>Recent rate reports</h6>
            {reports.map((report) => (
                <RateReport
                    key={report.uuid}
                    show_title={report.show_title}
                    season_number={report.season_number}
                    company={report.companies && report.companies[0]}
                    network={report.network}
                    union_status={unionStatus[report.union_status]}
                    genre={genre[report.genre]}
                    job_title={report.job_title_name}
                    day_rate={report.daily}
                    guarantee={report.guarantee}
                    hourly_rate={report.hourly}
                    increase={report.percent_increase}
                    start_date={report.season__start_date}
                />
            ))}
        </div>
    );
}
