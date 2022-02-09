import React from "react";
import Card from "react-bootstrap/Card";
import Badge from "react-bootstrap/Badge";

export default function RateReport({
    show_title,
    season_number,
    company,
    network,
    union_status,
    genre,
    job_title,
    day_rate,
    guarantee,
    hourly_rate,
    increase
}) {
    return (
        <div>
            <Card>
                <Card.Body>
                    <div className="d-flex mb-0 p-0">
                        <h5 className="m-0">{show_title}</h5>
                        <div className="ms-auto">
                            {increase &&
                            <Badge className="me-2" bg={"primary"}>+{increase}%</Badge>}
                        </div>
                        <h5 className="m-0">
                            ${day_rate}/{guarantee}
                        </h5>
                    </div>

                    <div className="d-flex">
                        <div className="me-auto">
                            <span>Season {season_number}</span>
                            <span>
                                <Badge className="ms-2" bg={"dark"}>
                                    {union_status}
                                </Badge>
                            </span>
                        </div>
                        <div className="ms-auto">
                            <span>${hourly_rate}/hr</span>
                        </div>
                    </div>

                    <div className="d-flex">
                        <span className="me-3">{company}</span>
                        <span>{network}</span>
                        <div className="ms-auto">
                            <span>{job_title}</span>
                        </div>
                    </div>
                </Card.Body>
            </Card>
        </div>
    );
}
