import React from "react";
import Card from "react-bootstrap/Card";
import Badge from "react-bootstrap/Badge";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import convertDate from "../common/convertDate"
import "./rate-report.css";

export default function RateReport({
    show_title,
    season_number,
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

                        <div className={""}>
                            <span className={"me-3"}>Season {season_number}</span>
                            <span className={"me-3"}>{convertDate(start_date, "numeric")}</span>
                            <span className={"me-3"}>{genre}</span>
                            <span className={"me-3"}>
                                <Badge bg={"dark"}>{union_status}</Badge>
                            </span>
                        </div>

                        <div className={"third-row"}>
                            {companies.length > 0 &&
                            <span className={companies.length === 1 && "me-3"}>{companies[0].name}</span>}
                            {companies.length > 1 &&
                            <span className={"me-3"}>&nbsp;(+{companies.length - 1} more...)</span>}
                            <span>
                                <Badge bg={"secondary"}>{network}</Badge>
                                {/*{network}*/}
                            </span>
                        </div>
                    </Card.Body>
                </Col>
            </Row>
        </Card>
    );
}
