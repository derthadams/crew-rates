import React from "react";
import "./report-container.css";
import RateReport from "./RateReport";
import Summary from './Summary';

export default function ReportContainer({ feed, summary, genre, unionStatus }) {

    return (
        <div className={"report-container d-flex py-1"}>
            <div id={"content-inner"}>
                {summary && summary.rate_count >= 3 &&
                <Summary summary={summary}/>}
                {feed.results && feed.results.length === 0 &&
                    <div className={"text-center mt-5"}>
                        <h3>No results</h3>
                    </div>}
                {feed.results && feed.results.map((result) => (
                    <RateReport
                        key={result.uuid}
                        start_date={result.start_date}
                        season_title={result.season_title}
                        union_status={unionStatus[result.union_status]}
                        genre={genre[result.genre]}
                        network_name={result.network_name}
                        company_list={result.company_list}
                        job_reports={result.job_reports}
                    />
                ))}
            </div>
        </div>
    );
}
