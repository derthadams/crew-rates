import React, {useState, useEffect, useLayoutEffect, useRef} from "react";
import DiscoverHeader from "./DiscoverHeader";
import ReportContainer from "./ReportContainer";
import axios from "axios";
import useObserver from "./useObserver";

export default function App() {
    const [feed, setFeed] = useState({});
    const [summary, setSummary] = useState({});
    const [dateRange, setDateRange] = useState(0);
    const [unionSelect, setUnionSelect] = useState('AA');
    const [genreSelect, setGenreSelect] = useState('AA');
    const [filter, setFilter] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const endOfFeed = useRef(null);
    const endOfFeedIsVisible = useObserver(endOfFeed);

    const appendResults = (newPage) => {
        setFeed(prevState => ({
                next: newPage.next,
                previous: newPage.previous,
                results: [
                    ...prevState.results,
                    ...newPage.results
                ]
            }));
    }

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
        setIsLoading(true);
        axios.get(url, {
            params: params
        })
             .then((response) => {
                 setIsLoading(false);
                 if(url !== apiUrls["season-list"]) {
                     appendResults(response.data);
                 } else {
                     setFeed(response.data);
                 }
        })
        ;
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
        getReports(params);
        getSummary(params);
    }, [dateRange, unionSelect, genreSelect, filter]);

    useEffect(() => {
        if(endOfFeedIsVisible && feed.results && feed.results.length > 0 && feed.next) {
            getReports({}, feed.next);
        }
    }, [endOfFeedIsVisible]);

    useLayoutEffect(() => {
        if(endOfFeedIsVisible && feed.next) {
            getReports({}, feed.next);
        }
    }, [feed]);

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
                             endOfFeed={endOfFeed}
                             isLoading={isLoading}
                             summary={summary}
                             genre={genre}
                             unionStatus={unionStatus}
                             genreSelect={genreSelect}
                             unionSelect={unionSelect}/>
        </div>
    );
}
