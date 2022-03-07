import React from "react";
import "./report-container.css";
import RateReport from "./RateReport";

export default function ReportContainer({ reports, unionStatus, genre }) {
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
                        season_title={report.show_title}
                        companies={report.companies}
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
        </div>
    );
}
