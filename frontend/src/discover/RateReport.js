import React from "react";

import Badge from "react-bootstrap/Badge";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup"
import convertDate from "../common/convertDate"
import "./rate-report.css";

export default function RateReport({
    season_title,
    companies,
    network,
    union_status,
    genre,
    job_title,
    day_rate,
    guarantee,
    hourly_rate,
    increase,
    start_date,
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
                    {companies.length > 0 &&
                        <span>{companies[0].name}</span>
                    }
                    <span className="ms-auto">
                        {convertDate(start_date, "numeric")}
                    </span>
                </div>
                {companies.length > 1 &&
                    <div>
                        {companies.slice(1,).map((company) => (
                            <span key={company.uuid}>{company.name}</span>
                        ))}
                    </div>}

                {/*Network and Genre*/}
                <div className="d-flex">
                    {network &&
                    <span className={"me-2"}>
                            <Badge bg={"secondary"}>
                                {network}
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
                    <ListGroup.Item>
                        <div className="d-flex">
                            <span>{job_title}</span>
                            <span className={"ms-auto"}>
                                {increase > 0 && (
                                    <Badge bg={"primary"} className={"me-1"}>
                                     &#8679;&nbsp;{increase}%
                                    </Badge>
                                )}
                                <strong>
                                    ${day_rate}/{guarantee}&nbsp;
                                </strong>
                                    (${hourly_rate}/hr)
                            </span>
                        </div>
                    </ListGroup.Item>

                </ListGroup>
            </Card.Body>

        </Card>
    );
}
