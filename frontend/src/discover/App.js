import React, { useState, useEffect } from "react";
import DiscoverHeader from "./DiscoverHeader";
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
    const genreOptions = JSON.parse(
        document.getElementById("genreOptions").textContent
    );
    const unionOptions = JSON.parse(
        document.getElementById("unionOptions").textContent
    )
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
        <div>
            <DiscoverHeader genreOptions={genreOptions}
                            unionOptions={unionOptions}/>
            <ReportContainer reports={reports}
                             genre={genre}
                             unionStatus={unionStatus} />
        </div>
    );
}
