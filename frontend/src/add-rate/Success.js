import React, { useEffect } from 'react';

import { Navigate, useLocation, useNavigate } from "react-router-dom";

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button"

import { useStateMachine } from "little-state-machine";
import { clearFormData } from "./UpdateFunctions";

function Success() {
    const locationState = useLocation();
    const { actions } = useStateMachine({clearFormData})
    const navigate = useNavigate();

    useEffect(() => {
        actions.clearFormData({});
    }, []);

    if( !locationState.state?.fromForm) {
        return <Navigate to="/" replace state={{fromForm: true}}/>
    }

    const handleAnotherRate = () => {
        navigate(`/`)
    }

    return (
        <div className="my-3">
            <h1 className="display-1">Thanks!</h1>
            <p>We appreciate you giving back to the community by submitting your rate report.</p>
            <p>Your report will appear on the site within 48 hours.</p>
            <Row className="mt-5">
                <Col className="col-3 col-sm-4"> </Col>
                <Col className="col-6 col-sm-4">
                    <Row>
                        <Button
                            variant="primary"
                            onClick={handleAnotherRate}
                        >Add another rate</Button>
                    </Row>
                </Col>
                <Col className="col-3 col-sm-4"> </Col>
            </Row>
        </div>
    )
}

export default Success;