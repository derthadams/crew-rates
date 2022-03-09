import React from "react";

import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import Row from "react-bootstrap/Row";

import Select from "react-select";

import "./discover-header.css";

export default function DiscoverHeader ({ genreOptions, unionOptions,
                                            dateRange, handleDateChange,
                                            unionSelect, handleUnionChange,
                                            genreSelect, handleGenreChange}) {
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
                                    value={dateRange}
                                    onChange={handleDateChange}
                                >
                                    <option value="6">6 months</option>
                                    <option value="12">12 months</option>
                                    <option value="24">2 years</option>
                                    <option value="0">Dates: All</option>
                                </Form.Select>
                                <Form.Select
                                    size={"sm"}
                                    name={"union-status"}
                                    id={"union-status"}
                                    value={unionSelect}
                                    onChange={handleUnionChange}
                                >
                                    <option value="AA">
                                        Union: All
                                    </option>
                                    {unionOptions.map((unionOption) => (
                                        <option key={unionOption.value} value={unionOption.value}>
                                            {unionOption.label}
                                        </option>
                                    ))}
                                </Form.Select>
                                <Form.Select
                                    size={"sm"}
                                    name={"genre-select"}
                                    id={"genre-select"}
                                    value={genreSelect}
                                    onChange={handleGenreChange}
                                >
                                    <option value="AA">
                                        Genre: All
                                    </option>
                                    {genreOptions.map((genreOption) => (
                                            <option key={genreOption.value}
                                                    value={genreOption.value}>
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