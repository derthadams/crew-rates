import React, { useState, useEffect } from 'react';

// import { useNavigate } from "react-router-dom";

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button"

import { useStateMachine } from "little-state-machine";
import {clearFormData} from "./UpdateFunctions";

function Success(props) {
    const { actions, state } = useStateMachine({clearFormData})
    // const navigate = useNavigate();

    useEffect(() => {
        actions.clearFormData({});
    }, []);

    const handleAnotherRate = () => {
        navigate(`/`)
    }

    return (
        <div className="my-3">
            <h1 className="display-1">Thanks!</h1>
            <p>We appreciate you submitting your rate report and giving back to the community!</p>
            <p>Your report will appear on the site within 48 hours.</p>
            <Row className="mt-5">
                <Col className="col-4"> </Col>
                <Col className="col-4">
                    <Row>
                        <Button
                            variant="success"
                            onClick={handleAnotherRate}
                        >Add Another Rate</Button>
                    </Row>
                </Col>
                <Col className="col-4"> </Col>
            </Row>
        </div>
    )
}

export default Success;