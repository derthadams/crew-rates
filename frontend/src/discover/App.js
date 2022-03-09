import React, { useState, useEffect } from "react";
import DiscoverHeader from "./DiscoverHeader";
import ReportContainer from "./ReportContainer";
import axios from "axios";

export default function App() {
    const [reports, setReports] = useState([]);
    const [dateRange, setDateRange] = useState(0);
    const [unionSelect, setUnionSelect] = useState('AA');
    const [genreSelect, setGenreSelect] = useState('AA');

    const handleDateChange = (event) => {
        setDateRange(parseInt(event.target.value));
    }

    const handleUnionChange = (event) => {
        setUnionSelect(event.target.value);
    }

    const handleGenreChange = (event) => {
        setGenreSelect(event.target.value);
    }

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
        axios.get(apiUrls["season-list"], {
            params: {
                date_range: dateRange,
                union_select: unionSelect,
                genre_select: genreSelect
            }
        }).then((response) => {
            const initialData = response.data;
            setReports(initialData);
        });
    };

    useEffect(() => {
        getInitialData();
    }, [dateRange, unionSelect, genreSelect]);

    return (
        <div>
            <DiscoverHeader genreOptions={genreOptions}
                            unionOptions={unionOptions}
                            dateRange={dateRange}
                            handleDateChange={handleDateChange}
                            unionSelect={unionSelect}
                            handleUnionChange={handleUnionChange}
                            genreSelect={genreSelect}
                            handleGenreChange={handleGenreChange}/>
            <ReportContainer reports={reports}
                             genre={genre}
                             unionStatus={unionStatus} />
        </div>
    );
}
