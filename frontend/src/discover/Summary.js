import React from 'react';

import Badge from 'react-bootstrap/Badge';
import Card from 'react-bootstrap/Card';

import Histogram from "./Histogram";
import './summary.css';

export default function Summary() {
    return (
            <Card className={"mb-1"}>
                <Card.Body>
                    <Card.Title className={"summary-heading d-flex mb-0"}>
                        <span>Camera Operator</span>
                        <span className={"ms-auto median-rate"}>$59.09/hr</span>
                    </Card.Title>

                    <div className={"d-flex mb-0"}>
                        <span>
                            <small>
                                9/20/2021-3/20/2022
                            </small>
                        </span>

                        <span className={"ms-auto"}>
                            <small>
                                Median rate
                            </small>
                        </span>
                    </div>

                    <div className={"d-flex"}>
                        <span>
                            <Badge bg={"dark"} className={"me-1 p-1"}>
                            <small>IATSE</small>
                            </Badge>
                            <small>
                                Reality
                            </small>
                        </span>

                        <span className={"ms-auto"}>
                            <small>
                                63 rates submitted
                            </small>
                        </span>
                    </div>

                </Card.Body>
                <div className={"px-3"}>
                    <Histogram/>
                </div>
                <div className={"px-3 mb-3"}>
                    <Card.Text className={"d-flex mb-n1"}>
                        <span>
                            $50.13
                        </span>
                        <span className={"ms-auto"}>
                            $95.00
                        </span>
                    </Card.Text>
                    <div className={"d-flex"}>
                        <span>
                            <small>
                                Low
                            </small>
                        </span>
                        <span className={"ms-auto"}>
                            <small>
                                High
                            </small>
                        </span>
                    </div>
                </div>

            </Card>
    )
}