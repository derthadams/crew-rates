import React from 'react';
import Badge from "react-bootstrap/Badge";
import ListGroup from "react-bootstrap/ListGroup";

export default function JobTitleReport({ report }) {
    const len = report.reports.length;
    const med = len % 2 === 0 ? len / 2 - 1 : Math.floor(len / 2)
    if (len === 1) {
        return (
            <ListGroup.Item>
                <div className="d-flex">
                    <span>{report.job_title.title}</span>
                    <span className={"ms-auto"}>
                        {report.reports[0].increase > 0 && (
                        <Badge bg={"primary"} className={"me-1"}>
                            &#8679;&nbsp;{report.reports[0].increase}%
                        </Badge>
                        )}

                        <strong>
                        ${report.reports[0].daily}/{report.reports[0].guarantee}&nbsp;
                        </strong>

                        (${report.reports[0].hourly.toFixed(2)}/hr)
                    </span>
                </div>
            </ListGroup.Item>
    )} else if (len >= 2) {
        return (
            <ListGroup.Item>
                <div className={"mb-1"}>
                    <span>{report.job_title.title}</span>
                </div>

                <div className="d-flex">
                    <span>
                    {report.reports[0].increase > 0 && (
                            <Badge bg={"primary"} className={"me-1 p-1"}>
                                &#8679;&nbsp;{report.reports[0].increase}%
                            </Badge>
                    )}
                            <strong>
                            ${report.reports[0].daily}/{report.reports[0].guarantee}&nbsp;
                            </strong>
                    </span>

                    {len >= 3 &&
                    <span className={"ms-auto"}>
                    {report.reports[med].increase > 0 && (
                            <Badge bg={"primary"} className={"me-1 p-1"}>
                                <small>&#8679;&nbsp;{report.reports[med].increase}%</small>
                            </Badge>
                    )}
                            <strong>
                            ${report.reports[med].daily}/
                            {report.reports[med].guarantee}&nbsp;
                            </strong>
                    </span>}

                    <span className={"ms-auto"}>
                    {report.reports[len - 1].increase > 0 && (
                            <Badge bg={"primary"} className={"me-1 p-1"}>
                                <small>&#8679;&nbsp;{report.reports[len - 1].increase}%</small>
                            </Badge>
                    )}
                            <strong>
                            ${report.reports[len - 1].daily}/{report.reports[len - 1].guarantee}&nbsp;
                            </strong>
                    </span>

                </div>

                <div className="d-flex mt-n1">
                    <span>
                        <small>(${report.reports[0].hourly.toFixed(2)}/hr)</small>
                    </span>
                    {len >= 3 &&
                    <span className={"ms-auto"}>
                        <small>(${report.reports[med].hourly.toFixed(2)}/hr)</small>
                    </span>}
                    <span className={"ms-auto"}>
                        <small>(${report.reports[len - 1].hourly.toFixed(2)}/hr)</small>
                    </span>
                </div>


                <div className="d-flex mt-n1">
                    <span>
                        <small>Low</small>
                    </span>
                    {len >= 3 &&
                    <span className="ms-auto">
                        <small>Median</small>
                    </span>}
                    <span className="ms-auto">
                        <small>High</small>
                    </span>
                </div>

            </ListGroup.Item>
        )
    }
}