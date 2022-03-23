import React from 'react';

import Badge from 'react-bootstrap/Badge';
import Card from 'react-bootstrap/Card';

import Histogram from "./Histogram";
import convertDate from "../common/convertDate";
import './summary.css';

export default function Summary({ summary }) {
    return (
        <Card className={"mb-1"}>
            <Card.Body>
                <Card.Title className={"summary-heading d-flex mb-0"}>
                    <span>{summary.heading}</span>
                    <span className={"ms-auto median-rate"}>
                        ${summary.statistics.med.toFixed(2)}/hr
                    </span>
                </Card.Title>

                <div className={"d-flex mb-0"}>
                    <span>
                        <small>{summary.start_date ?
                                convertDate(summary.start_date, 'numeric') + " - Present"
                                : "All Dates"}
                        </small>
                    </span>

                    <span className={"ms-auto"}>
                        <small>Median rate</small>
                    </span>
                </div>

                <div className={"d-flex"}>
                    <span>
                        <Badge bg={"dark"} className={"me-1 p-1"}>
                            <small>{summary.union_title}</small>
                        </Badge>
                        <small>{summary.genre_title}</small>
                    </span>

                    <span className={"ms-auto"}>
                        <small>{summary.rate_count} rates submitted</small>
                    </span>
                </div>
            </Card.Body>
            <div className={"px-3"}>
                <Histogram histogram={summary.histogram}/>
            </div>
            <div className={"px-3 mb-3"}>
                <Card.Text className={"d-flex mb-n1"}>
                    <span>${summary.statistics.min.toFixed(2)}</span>
                    <span className={"ms-auto"}>
                        ${summary.statistics.max.toFixed(2)}</span>
                </Card.Text>
                <div className={"d-flex"}>
                    <span>
                        <small>Low</small>
                    </span>
                    <span className={"ms-auto"}>
                        <small>High</small>
                    </span>
                </div>
            </div>
        </Card>
    );
}