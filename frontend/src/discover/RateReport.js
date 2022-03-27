import React from "react";

import Badge from "react-bootstrap/Badge";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup"
import convertDate from "../common/convertDate"

import JobTitleReport from "./JobTitleReport";
import "./rate-report.css";

export default function RateReport({
    start_date,
    season_title,
    union_status,
    genre,
    network_name,
    company_list,
    job_reports
}) {
    return (
        <Card className={"mb-1"}>
            <Card.Header>

                {/*Season Title and Union Status*/}
                <div className="d-flex">
                    <span>
                        <Card.Title className={"me-3"}>
                            {season_title}
                        </Card.Title>
                    </span>

                    {union_status &&
                    <span className="ms-auto">
                        <Badge bg={"dark"} className={"me-1"}>
                            {union_status}
                        </Badge>
                    </span>}
                </div>

                {/*Companies and Start Date*/}
                <div className="d-flex">
                    {/*{companies.length > 0 &&*/}
                    {/*    <span className={`${companies.length === 1 ? "me-2" : ""}`}>*/}
                    {/*        {companies[0].name}*/}
                    {/*    </span>}*/}
                    {/*{companies.length > 1 &&*/}
                    {/*    <span className={"me-2"}>*/}
                    {/*        /!*&nbsp;(+{companies.length - 1})*!/*/}
                    {/*        &nbsp;...*/}
                    {/*    </span>}*/}
                    {company_list.length > 0 &&
                        <span>{company_list[0].name}</span>
                    }
                    <span className="ms-auto">
                        {convertDate(start_date, "numeric")}
                    </span>
                </div>
                {company_list.length > 1 &&
                    <div>
                        {company_list.slice(1,).map((company) => (
                            <span key={company.uuid}>{company.name}</span>
                        ))}
                    </div>}

                {/*Network and Genre*/}
                <div className="d-flex">
                    {network_name &&
                    <span className={"me-2"}>
                            <Badge bg={"secondary"}>
                                {network_name}
                            </Badge>
                        </span>}
                    {genre &&
                    <span className={"ms-auto"}>
                            {genre}
                        </span>}
                </div>
            </Card.Header>

            <Card.Body className={"p-0"}>
                <ListGroup variant={"flush"}>

                    {/*Job Report*/}

                    {job_reports.map((report) => <JobTitleReport key={report.job_title.uuid}
                                                                 report={report}/>)}
                </ListGroup>
            </Card.Body>

        </Card>
    );
}
