import React from "react";
import "./report-container.css";
import RateReport from "./RateReport";

export default function ReportContainer({ reports, genre, unionStatus, genreSelect, unionSelect }) {
    return (
        <div className={"report-container d-flex py-1"}>
            <div id={"content-inner"}>
                {reports.length === 0 &&
                    <div className={"text-center mt-5"}>
                        <h3>No results</h3>
                    </div>}
                {reports.map((report) => (
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
