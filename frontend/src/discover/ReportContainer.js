import React from "react";
import "./report-container.css";
import RateReport from "./RateReport";
import Summary from './Summary';

export default function ReportContainer({ feed, genre, unionStatus, genreSelect, unionSelect }) {
    const summaryUnion = unionSelect === 'AA' ? 'Union and Non-Union' : unionStatus[unionSelect];
    const summaryGenre = genreSelect === 'AA' ? 'All Genres' : genre[genreSelect];

    return (
        <div className={"report-container d-flex py-1"}>
            <div id={"content-inner"}>
                {feed.summary && feed.summary.rate_count >= 3 &&
                <Summary summary={feed.summary}
                         genre={summaryGenre}
                         union_status={summaryUnion}
                         heading={feed.reports[0].job_reports[0].job_title.title}/>}
                {feed.reports && feed.reports.length === 0 &&
                    <div className={"text-center mt-5"}>
                        <h3>No results</h3>
                    </div>}
                {feed.reports && feed.reports.map((report) => (
                    <RateReport
                        key={report.uuid}
                        start_date={report.start_date}
                        season_title={report.season_title}
                        union_status={unionStatus[report.union_status]}
                        genre={genre[report.genre]}
                        network_name={report.network_name}
                        company_list={report.company_list}
                        job_reports={report.job_reports}
                    />
                ))}
            </div>
        </div>
    );
}
