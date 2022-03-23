import React, { useState, useEffect } from "react";
import DiscoverHeader from "./DiscoverHeader";
import ReportContainer from "./ReportContainer";
import axios from "axios";

export default function App() {
    const [feed, setFeed] = useState({});
    const [summary, setSummary] = useState({});
    const [dateRange, setDateRange] = useState(0);
    const [unionSelect, setUnionSelect] = useState('AA');
    const [genreSelect, setGenreSelect] = useState('AA');
    const [filter, setFilter] = useState({});

    const handleDateChange = (event) => {
        setDateRange(parseInt(event.target.value));
    }

    const handleUnionChange = (event) => {
        setUnionSelect(event.target.value);
    }

    const handleGenreChange = (event) => {
        setGenreSelect(event.target.value);
    }

    const handleFilterChange = (newValue) => {
        setFilter(newValue);
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

    const getReports = (params, url=apiUrls["season-list"]) => {
        console.log("url", url);
        axios.get(url, {
            params: params
        })
             .then((response) => {
                 setFeed(response.data)
        });
    };

    const getSummary = (params) => {
        axios.get(apiUrls["summary"], {
            params: params
        })
                .then((response) => {
                    setSummary(response.data)
                })
    }

    useEffect(() => {
        const params = {
            date_range: dateRange,
            union_select: unionSelect,
            genre_select: genreSelect,
            filter_uuid: filter ? filter.value : "",
            filter_type: filter ? filter.type : ""
        }
        console.log("params", params);
        getReports(params);
        getSummary(params);
    }, [dateRange, unionSelect, genreSelect, filter]);

    return (
        <div>
            <DiscoverHeader genreOptions={genreOptions}
                            unionOptions={unionOptions}
                            dateRange={dateRange}
                            handleDateChange={handleDateChange}
                            unionSelect={unionSelect}
                            handleUnionChange={handleUnionChange}
                            genreSelect={genreSelect}
                            handleGenreChange={handleGenreChange}
                            filter={filter}
                            handleFilterChange={handleFilterChange}
                            searchURL={apiUrls["filter-search"]}/>
            <ReportContainer feed={feed}
                             summary={summary}
                             genre={genre}
                             unionStatus={unionStatus}
                             genreSelect={genreSelect}
                             unionSelect={unionSelect}/>
        </div>
    );
}
