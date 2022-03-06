import React from "react";

import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import Row from "react-bootstrap/Row";

import Select from "react-select";

import "./discover-header.css";

export default function DiscoverHeader () {
    return (
        <div className={"sticky-top"}>
            <div className={"bg-light pt-1 pb-2"}>
                <div className="px-2">
                    <Row>
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
                                    <option value="1">Default</option>
                                </Form.Select>
                                <Form.Select
                                    size={"sm"}
                                    name={"union-status"}
                                    id={"union-status"}
                                >
                                    <option value="1">Default</option>
                                </Form.Select>
                                <Form.Select
                                    size={"sm"}
                                    name={"genre-select"}
                                    id={"genre-select"}
                                >
                                    <option value="1">Default</option>
                                </Form.Select>
                            </InputGroup>
                        </Col>
                    </Row>
                </div>
            </div>
        </div>
    )
}