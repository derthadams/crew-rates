import React, { useState } from 'react';

import { useNavigate } from "react-router-dom";

import { useForm, useFormContext, FormProvider, Controller } from "react-hook-form"
import { ErrorMessage } from "@hookform/error-message";

import { useStateMachine } from "little-state-machine";

import Form from "react-bootstrap/Form"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import ProgressBar from "react-bootstrap/ProgressBar"
import Button from "react-bootstrap/Button"
import ToggleButtonGroup from "react-bootstrap/ToggleButtonGroup";
import ToggleButton from "react-bootstrap/ToggleButton";

import "./survey.css"
import AsyncAPISelect from "./AsyncAPISelect";
import {updateFormData} from "./UpdateFunctions";
import RateWidget from "./RateWidget";

function PageTwo(props) {
    const { actions, state } = useStateMachine({updateFormData})
    const methods = useForm(
        {
            defaultValues: state.formData
        }
    );
    const [negotiated, setNegotiated] = useState(methods.getValues('negotiated'));
    const [increased, setIncreased] = useState(methods.getValues('increased'));
    const apiUrls = JSON.parse(document.getElementById('apiUrls').textContent);

    let navigate = useNavigate();

    const convertStrToInt = (data) => {
        if(data['offered_guarantee'] !== '') {
            data['offered_guarantee'] = parseInt(data['offered_guarantee'], 10);
        }
        if(data['final_guarantee'] !== '') {
            data['final_guarantee'] = parseInt(data['final_guarantee'], 10);
        }
        return data
    }

    const handleNegotiatedChange = (value) => {
        setNegotiated(value);
        if(value === false) {
            setIncreased(false);
            methods.setValue('increased', '')
        }
    }

    const handleIncreasedChange = (value) => {
        setIncreased(value);
    }

    const validateNegotiated = () => {
        if(methods.getValues('negotiated') === '') {
            methods.setError('negotiated', {
                type: 'manual',
                message: 'This question is required'
            });
        }
    }

    const validateIncreased = () => {
        if(methods.getValues('increased') === '' && (negotiated || methods.getValues('negotiated'))) {
            methods.setError('increased', {
                type: 'manual',
                message: 'This question is required'
            });
        }
    }

    const onSubmit = (data) => {
        actions.updateFormData(convertStrToInt(data));
        navigate(`/3`);
    };

    return (
        <div className='my-3'>
            <h1 className="display-1">Add a rate</h1>
            <p>Your anonymous rate information will help all crew members
                negotiate better deals.</p>
            <h6 className="display-6">Rate information</h6>
            <ProgressBar now={66} label=" Step 2 of 3" className="mx-6 my-3"/>
            <FormProvider {...methods}>
            <Form noValidate onSubmit={methods.handleSubmit((data) => {
                validateNegotiated();
                validateIncreased();
                onSubmit(data);
            })}>
                <Row>
                    <Form.Group className="mb-3" controlId="jobTitle">
                        <Form.Label className="required-label">What was your job title on the show?</Form.Label>
                        <Controller
                            name='job_title'
                            control={methods.control}
                            rules={{required: "Job title is required"}}
                            render={({   field ,
                                         fieldState}) =>
                                <AsyncAPISelect
                                    {...field}
                                    {...fieldState}
                                    lsmValue={state.formData.job_title}
                                    creatable={true}
                                    url={apiUrls['job-titles']}
                                    search_text="a job title"
                                    callback={(response) => response.data}
                                />
                            } />
                        <ErrorMessage
                            errors={methods.formState.errors}
                            name='job_title'
                            render = {
                                ({ message }) =>
                                    <Form.Text className="text-danger">{message}</Form.Text>
                            }
                        />
                    </Form.Group>
                </Row>
                <Row>
                    <Form.Label className="required-label">
                        What rate were you first offered?
                    </Form.Label>
                </Row>


                <RateWidget
                    name="offered"
                />

                <Row className="mb-2">
                    <Col xs={9}>
                        <Form.Label className="required-label">
                            Did you try to negotiate a higher rate?
                        </Form.Label>
                    </Col>
                    <Col xs={3}>
                        <Controller
                            name='negotiated'
                            control={methods.control}
                            render = {({    field}) =>
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
                                    <ToggleButton id="negotiated_yes" value={true}
                                                  variant="outline-dark">Yes</ToggleButton>
                                    <ToggleButton id="negotiated_no" value={false}
                                                  variant="outline-dark">No</ToggleButton>
                                </ToggleButtonGroup>
                            }
                        />
                    </Col>
                    <ErrorMessage
                        errors={methods.formState.errors}
                        name='negotiated'
                        render = {
                            ({ message }) =>
                                <Form.Text className="text-danger">{message}</Form.Text>
                        }
                    />
                </Row>

                {(negotiated || methods.getValues('negotiated')) ?
                    (
                        <Row className="mb-2">
                            <Col xs={9}>
                                <Form.Label className="required-label">
                                    Did you get a higher rate?
                                </Form.Label>
                            </Col>
                            <Col xs={3}>
                                <Controller
                                    name='increased'
                                    control={methods.control}
                                    render = {({field}) =>
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
                                            <ToggleButton id="increased_yes" value={true}
                                                          variant="outline-dark">Yes</ToggleButton>
                                            <ToggleButton id="increased_no" value={false}
                                                          variant="outline-dark">No</ToggleButton>
                                        </ToggleButtonGroup>
                                    }
                                />
                            </Col>
                            <ErrorMessage
                                errors={methods.formState.errors}
                                name='increased'
                                render = {
                                    ({ message }) =>
                                        <Form.Text className="text-danger">{message}</Form.Text>
                                }
                            />
                        </Row>
                    ) :
                    <div> </div>
                }

                {((negotiated || methods.getValues('negotiated')) && (increased || methods.getValues('increased'))) ?
                    (<div>
                        <Row>
                        <Form.Label className="required-label">
                            Congratulations! What was the final rate?
                        </Form.Label>
                    </Row>
                    <RateWidget
                        name="final"
                    />
                    </div>
                    ) :
                    <div> </div>
                }

                <Row className="mt-3">
                    <Col xs={3}>
                        <Row className="mx-0">
                            <Button
                                size="sm"
                                onClick={()=>{
                                    actions.updateFormData(convertStrToInt(methods.getValues()))
                                    navigate(-1, {replace: false});
                                }}
                            >Previous</Button>
                        </Row>
                    </Col>
                    <Col xs={6}>
                    </Col>
                    <Col xs={3}>
                        <Row className="mx-0">
                            <Button type="submit" size="sm">Next</Button>
                        </Row>
                    </Col>
                </Row>

            </Form>
            </FormProvider>
        </div>
    )
}

export default PageTwo;