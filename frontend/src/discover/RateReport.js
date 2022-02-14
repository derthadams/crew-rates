import React from "react";
import Card from "react-bootstrap/Card";
import Badge from "react-bootstrap/Badge";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import convertDateNumeric from "./convertDateNumeric";
import "./rate-report.css";

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
    increase,
    start_date,
}) {
    return (
        <Card className="mb-3" style={{ maxWidth: 648 }}>
            <Row className="g-0">
                <Col
                    className="md-4"
                    xs={4}
                    style={{ backgroundColor: "lightgray" }}
                >
                    <Card.Body className={"text-end"}>
                        <div>
                            <span className={"first-row"}>
                                ${day_rate}/{guarantee}
                            </span>
                        </div>

                        <div>
                            <span className={"me-1"}>
                                {increase && (
                                    <Badge bg={"primary"}>
                                        &#8679;&nbsp;{increase}%
                                    </Badge>
                                )}
                            </span>
                            <span className={""}>${hourly_rate}/hr</span>
                        </div>

                        <div className={"third-row"}>
                            <span>{job_title}</span>
                        </div>
                    </Card.Body>
                </Col>

                <Col className="md-8" xs={8}>
                    <Card.Body>
                        <div className="show-row">
                            <span className={"first-row"}>{show_title}</span>
                        </div>

                        <div>
                            <span className={"me-3"}>Season {season_number}</span>
                            <span className={"me-3"}>{convertDateNumeric(start_date)}</span>
                            <span className={"me-3"}>{genre}</span>
                            <span className={"me-3"}>
                                <Badge bg={"dark"}>{union_status}</Badge>
                            </span>
                        </div>

                        <div className={"third-row"}>
                            <span className={"me-3"}>{company}</span>
                            <span>
                                <Badge bg={"secondary"}>{network}</Badge>
                            </span>
                        </div>
                    </Card.Body>
                </Col>
            </Row>
        </Card>
    );
}
