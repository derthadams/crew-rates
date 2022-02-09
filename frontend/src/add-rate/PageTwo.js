import React, { useState } from "react";

import { Navigate, useNavigate, useLocation } from "react-router-dom";

import {
    useForm,
    FormProvider,
    Controller,
} from "react-hook-form";
import { ErrorMessage } from "@hookform/error-message";

import { useStateMachine } from "little-state-machine";

import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import ProgressBar from "react-bootstrap/ProgressBar";
import Button from "react-bootstrap/Button";
import ToggleButtonGroup from "react-bootstrap/ToggleButtonGroup";
import ToggleButton from "react-bootstrap/ToggleButton";

import "./survey.css";
import AsyncAPISelect from "./AsyncAPISelect";
import { updateFormData } from "./UpdateFunctions";
import RateWidget from "./RateWidget";
import AddRateHeading from "./AddRateHeading";

function PageTwo() {
    const locationState = useLocation();
    const { actions, state } = useStateMachine({ updateFormData });
    const methods = useForm({
        defaultValues: state.formData,
    });
    const [negotiated, setNegotiated] = useState(
        methods.getValues("negotiated")
    );
    const [increased, setIncreased] = useState(methods.getValues("increased"));
    let navigate = useNavigate();
    if (!locationState.state?.fromForm) {
        return <Navigate to="/" replace state={{ fromForm: true }} />;
    }

    const apiUrls = JSON.parse(document.getElementById("apiUrls").textContent);

    const convertStrToInt = (data) => {
        if (data["offered_guarantee"] !== "") {
            data["offered_guarantee"] = parseInt(data["offered_guarantee"], 10);
        }
        if (data["final_guarantee"] !== "") {
            data["final_guarantee"] = parseInt(data["final_guarantee"], 10);
        }
        return data;
    };

    const handleNegotiatedChange = async (value) => {
        setNegotiated(value);
        if (value === false) {
            setIncreased(false);
            methods.setValue("increased", "");
            clearFinalRate();
        }
        if (methods.formState.errors["negotiated"]) {
            await methods.trigger("negotiated")
        }
    };

    const handleIncreasedChange = async (value) => {
        setIncreased(value);
        if(value === false) {
            clearFinalRate();
        }
        if (methods.formState.errors["increased"]) {
            await methods.trigger("increased")
        }
    };

    const clearFinalRate = () => {
        methods.setValue("final_day_rate", "");
        methods.setValue("final_guarantee", "");
        methods.setValue("final_hourly_rate", "")
    }

    const validateNegotiated = () => {
        if (methods.getValues("negotiated") === "") {
            methods.setError("negotiated", {
                type: "manual",
                message: "This question is required",
            });
        }
    };

    const validateIncreased = () => {
        if (
            methods.getValues("increased") === "" &&
            (negotiated || methods.getValues("negotiated"))
        ) {
            methods.setError("increased", {
                type: "manual",
                message: "This question is required",
            });
        }
    };

    const onSubmit = (data) => {
        actions.updateFormData(convertStrToInt(data));
        navigate(`/3`, { state: { fromForm: true } });
    };

    return (
        <div className="my-3">
            <AddRateHeading subheading={"Rate information"} now={66} label={"Step 2 of 3"}/>
            <FormProvider {...methods}>
                <Form
                    noValidate
                    aria-label="add-rate-2"
                    onSubmit={async (event) => {
                        event.preventDefault()
                        await methods.trigger();
                        validateNegotiated();
                        validateIncreased();
                        if(Object.keys(methods.formState.errors).length === 0) {
                            await methods.handleSubmit(onSubmit)()
                        }
                    }}
                >
                    <Row>
                        <Form.Group className="mb-3" controlId="jobTitle">
                            <Form.Label
                                className="required-label"
                                id="job-title-label"
                            >
                                What was your job title on the show?
                            </Form.Label>
                            <Controller
                                name="job_title"
                                control={methods.control}
                                rules={{ required: "Job title is required" }}
                                render={({ field, fieldState }) => (
                                    <AsyncAPISelect
                                        ariaLabelledby="job-title-label"
                                        {...field}
                                        {...fieldState}
                                        lsmValue={state.formData.job_title}
                                        creatable={true}
                                        url={apiUrls["job-titles"]}
                                        search_text="a job title"
                                        callback={(response) => response.data}
                                        onChange={async (inputValue, action) => {
                                            field.onChange(inputValue, action);
                                            if(methods.formState.errors["job_title"]) {
                                                await methods.trigger("job_title");
                                            }
                                        }}
                                    />
                                )}
                            />
                            <ErrorMessage
                                errors={methods.formState.errors}
                                name="job_title"
                                render={({ message }) => (
                                    <Form.Text className="text-danger">
                                        {message}
                                    </Form.Text>
                                )}
                            />
                        </Form.Group>
                    </Row>
                    <Row>
                        <Form.Label className="required-label">
                            What rate were you first offered?
                        </Form.Label>
                    </Row>

                    <RateWidget name="offered" />

                    <Row className="mb-2">
                        <Col xs={9}>
                            <Form.Label className="required-label">
                                Did you try to negotiate a higher rate?
                            </Form.Label>
                        </Col>
                        <Col xs={3}>
                            <Controller
                                name="negotiated"
                                control={methods.control}
                                render={({ field }) => (
                                    <ToggleButtonGroup
                                        {...field}
                                        name="negotiated"
                                        type="radio"
                                        size="sm"
                                        onChange={(value) => {
                                            field.onChange(value);
                                            handleNegotiatedChange(value);
                                        }}
                                    >
                                        <ToggleButton
                                            id="negotiated_yes"
                                            aria-label="negotiated_yes"
                                            value={true}
                                            variant="outline-dark"
                                        >
                                            Yes
                                        </ToggleButton>
                                        <ToggleButton
                                            id="negotiated_no"
                                            aria-label="negotiated_no"
                                            value={false}
                                            variant="outline-dark"
                                        >
                                            No
                                        </ToggleButton>
                                    </ToggleButtonGroup>
                                )}
                            />
                        </Col>
                        <ErrorMessage
                            errors={methods.formState.errors}
                            name="negotiated"
                            render={({ message }) => (
                                <Form.Text className="text-danger">
                                    {message}
                                </Form.Text>
                            )}
                        />
                    </Row>

                    {negotiated || methods.getValues("negotiated") ? (
                        <Row className="mb-2">
                            <Col xs={9}>
                                <Form.Label className="required-label">
                                    Did you get a higher rate?
                                </Form.Label>
                            </Col>
                            <Col xs={3}>
                                <Controller
                                    name="increased"
                                    control={methods.control}
                                    render={({ field }) => (
                                        <ToggleButtonGroup
                                            {...field}
                                            name="increased"
                                            type="radio"
                                            size="sm"
                                            onChange={(value) => {
                                                field.onChange(value);
                                                handleIncreasedChange(value);
                                            }}
                                        >
                                            <ToggleButton
                                                id="increased_yes"
                                                aria-label="increased_yes"
                                                value={true}
                                                variant="outline-dark"
                                            >
                                                Yes
                                            </ToggleButton>
                                            <ToggleButton
                                                id="increased_no"
                                                aria-label="increased_no"
                                                value={false}
                                                variant="outline-dark"
                                            >
                                                No
                                            </ToggleButton>
                                        </ToggleButtonGroup>
                                    )}
                                />
                            </Col>
                            <ErrorMessage
                                errors={methods.formState.errors}
                                name="increased"
                                render={({ message }) => (
                                    <Form.Text className="text-danger">
                                        {message}
                                    </Form.Text>
                                )}
                            />
                        </Row>
                    ) : (
                        <div></div>
                    )}

                    {(negotiated || methods.getValues("negotiated")) &&
                    (increased || methods.getValues("increased")) ? (
                        <div>
                            <Row>
                                <Form.Label className="required-label">
                                    Congratulations! What was the final rate?
                                </Form.Label>
                            </Row>
                            <RateWidget name="final" />
                        </div>
                    ) : (
                        <div></div>
                    )}

                    <Row className="mt-3">
                        <Col xs={3}>
                            <Row className="mx-0">
                                <Button
                                    size="sm"
                                    onClick={() => {
                                        actions.updateFormData(
                                            convertStrToInt(methods.getValues())
                                        );
                                        navigate(-1, {
                                            replace: false,
                                            state: { fromForm: true },
                                        });
                                    }}
                                >
                                    Previous
                                </Button>
                            </Row>
                        </Col>
                        <Col xs={6}></Col>
                        <Col xs={3}>
                            <Row className="mx-0">
                                <Button
                                    type="submit"
                                    size="sm">
                                    Next
                                </Button>
                            </Row>
                        </Col>
                    </Row>
                </Form>
            </FormProvider>
        </div>
    );
}

export default PageTwo;
