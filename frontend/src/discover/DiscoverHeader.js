import React from "react";

import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import Row from "react-bootstrap/Row";

import Select from "react-select";

import "./discover-header.css";

export default function DiscoverHeader ({ genreOptions, unionOptions }) {
    return (
        <div className={"sticky-top header-wrapper"}>
            <div className={"bg-light pt-1 pb-2"}>
                <div className="">
                    <Row className={"discover-nav-row"}>
                        <Col md={6}>
                            <Select
                                placeholder={"Filter by show, company, network, job title"}
                            />
                        </Col>
                        <Col md={6} className={"mt-2 mt-sm-1"}>
                            <InputGroup>
                                <Form.Select
                                    size={"sm"}
                                    name={"date-range"}
                                    id={"date-range"}
                                >
                                    <option value="6" selected>6 months</option>
                                    <option value="12">12 months</option>
                                    <option value="24">2 years</option>
                                    <option value="AA">All</option>
                                </Form.Select>
                                <Form.Select
                                    size={"sm"}
                                    name={"union-status"}
                                    id={"union-status"}
                                >
                                    <option value="AA">
                                        Union: All
                                    </option>
                                    {unionOptions.map((unionOption) => (
                                        <option value={unionOption.value}>
                                            {unionOption.label}
                                        </option>
                                    ))}
                                </Form.Select>
                                <Form.Select
                                    size={"sm"}
                                    name={"genre-select"}
                                    id={"genre-select"}
                                >
                                    <option value="AA">
                                        Genre: All
                                    </option>
                                    {genreOptions.map((genreOption) => (
                                            <option value={genreOption.value}>
                                                {genreOption.label}
                                            </option>
                                    ))}
                                </Form.Select>
                            </InputGroup>
                        </Col>
                    </Row>
                </div>
            </div>
        </div>
    )
}