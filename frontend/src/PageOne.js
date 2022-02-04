import React from 'react';

import { useNavigate } from "react-router-dom";

import { useForm, Controller } from "react-hook-form"
import { ErrorMessage } from "@hookform/error-message";

import { useStateMachine } from "little-state-machine";

import Form from "react-bootstrap/Form"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import ProgressBar from "react-bootstrap/ProgressBar"
import Button from "react-bootstrap/Button"

import Select from 'react-select'

import axios from 'axios'

import {v4 as uuid_v4} from "uuid";

import "./survey.css"
import AsyncAPISelect from "./AsyncAPISelect";
import customStyles from "./CustomSelectStyles";
import { updateLocationDetails, updateFormData } from "./UpdateFunctions";

function PageOne() {
    const { actions, state } = useStateMachine({ updateLocationDetails, updateFormData });
    const { control, handleSubmit, formState: { errors }, getValues } = useForm(
        {
            defaultValues: state.formData
        }
    );
    let navigate = useNavigate();
    let sessionToken = newSessionToken();
    const genreOptions = JSON.parse(document.getElementById('genreOptions').textContent);
    const unionOptions = JSON.parse(document.getElementById('unionOptions').textContent);
    const apiUrls = JSON.parse(document.getElementById('apiUrls').textContent);

    function newSessionToken() {
        return uuid_v4();
    }

    const handleLocationChange = (inputValue, {action, }) => {
        if(action === 'select-option') {
            if(inputValue.length > 0) {
                let selected = inputValue.slice(-1)[0];
                let place_id = selected.value;
                axios.get(apiUrls['details'], {
                    params: {
                        q: place_id,
                        sessiontoken: sessionToken
                    }
                }).then(response => {
                    let scopes = response.data.result.address_components.map(item => {
                        return {
                            long_name: item.long_name,
                            short_name: item.short_name,
                            type: item.types[0]
                        };
                    });
                    for(let i = 0; i < scopes.length; i++) {
                        let display_name = scopes[i].long_name;
                        for(let j = i +1; j < scopes.length; j++) {
                            if(scopes[j].type === 'administrative_area_level_1' ||
                                scopes[j].type === 'country') {
                                display_name += ", " + scopes[j].short_name;
                            }
                        }
                        scopes[i]["display_name"] = display_name;
                    }
                    actions.updateLocationDetails({
                        key: place_id,
                        value: {
                                    display_name: response.data.result.formatted_address,
                                    scopes: scopes
                                }
                    })
                    sessionToken = newSessionToken()
                });
            }
        }
    }

    const getSessionToken = () => {
        return sessionToken;
    }

    const onSubmit = (data) => {
        actions.updateFormData(data);
        navigate(`/2`, {state: {fromForm: true}});
    };

    return (
        <div className="my-3">
            <h1 className="display-1">Add a rate</h1>

            <p>Your anonymous rate information will help all crew members
                negotiate better deals.</p>
            <h6 className="display-6">Show information</h6>

            <ProgressBar now={33} label=" Step 1 of 3" className="mx-6 my-3"/>

            <Form noValidate onSubmit={handleSubmit(onSubmit)} aria-label="add-rate-1">
            <Row className="mt-4">
                <Col xs={9}>
                    <Form.Group className="mb-3" controlId="showTitle">
                        <Form.Label className="required-label"
                                    id="show-label">
                            Show title
                        </Form.Label>
                        <Controller
                            name='show_title'
                            control={control}
                            rules={{required: "Show title is required"}}
                            render={({   field ,
                                         fieldState: { invalid }}) =>
                                <AsyncAPISelect
                                    ariaLabelledby="show-label"
                                    {...field}
                                    invalid={invalid}
                                    lsmValue={state.formData.show_title}
                                    creatable={true}
                                    url={apiUrls['shows']}
                                    search_text="a show"
                                    callback={(response) => response.data}
                                />
                            } />
                        <ErrorMessage
                            errors={errors}
                            name='show_title'
                            render = {
                                ({ message }) =>
                                    <Form.Text className="text-danger">{message}</Form.Text>
                            }
                        />
                    </Form.Group>
                </Col>
                <Col xs={3}>
                    <Form.Group className="mb-3" controlId="seasonNum">
                        <Form.Label className="required-label">Season</Form.Label>
                        <Controller
                            name='season_number'
                            control={control}
                            rules={{
                                required: {
                                    value: true,
                                    message: "Season is required"
                                },
                                min: {
                                    value: 1,
                                    message: "Season must be 1 or greater"
                                }
                            }}
                            render={({   field ,
                                         fieldState: { invalid }}) =>
                            <Form.Control
                                {...field}
                                type="number"
                                isInvalid={invalid}
                                onChange={(event) => {
                                    field.onChange(event.target.value)
                                }}
                            />}
                        />
                        <ErrorMessage
                            errors={errors}
                            name='season_number'
                            render = {
                                ({ message }) => <Form.Text className="text-danger">{message}</Form.Text>
                            }
                        />
                    </Form.Group>
                </Col>
            </Row>

            <Row>
                <Col xs={6}>
                    <Form.Group className="mb-3" controlId="startDate">
                        <Form.Label className="required-label">Start date</Form.Label>
                        <Controller
                            name='start_date'
                            control={control}
                            rules={{
                                required: {
                                    value: true,
                                    message: 'Start date is required'
                                }
                            }}
                            render={({   field ,
                                         fieldState: { invalid }}) =>
                                <Form.Control
                                    {...field}
                                    type="date"
                                    isInvalid={invalid}
                                />}
                        />
                        <ErrorMessage
                            errors={errors}
                            name='start_date'
                            render = {
                                ({ message }) =>
                                    <Form.Text className="text-danger">{message}</Form.Text>
                            }
                        />
                    </Form.Group>
                </Col>
                <Col xs={6}>
                    <Form.Group className="mb-3" controlId="endDate">
                        <Form.Label>End date</Form.Label>
                        <Controller
                            name='end_date'
                            control={control}
                            rules={{
                                validate: {
                                    endAfterStart: (v) =>
                                        getValues('end_date') === '' ||
                                        new Date(getValues('end_date')) >= new Date(getValues('start_date')) ||
                                        "End date should be later than start date"
                                }
                            }}
                            render={({   field ,
                                         fieldState: { invalid }}) =>
                                <Form.Control
                                    {...field}
                                    type="date"
                                    isInvalid={invalid}
                                />}
                        />
                        <ErrorMessage
                            errors={errors}
                            name='end_date'
                            render = {
                                ({ message }) =>
                                    <Form.Text className="text-danger">{message}</Form.Text>
                            }
                        />
                    </Form.Group>
                </Col>
            </Row>

            <Row>
                <Form.Group className="mb-3" controlId="companies">
                    <Form.Label id="companies-label">Production companies</Form.Label>
                    <Controller
                        name='companies'
                        control={control}
                        render={({   field ,
                                     fieldState: { invalid }}) =>
                        <AsyncAPISelect
                            ariaLabelledby="companies-label"
                            {...field}
                            lsmValue={state.formData.companies}
                            creatable={true}
                            isMulti={true}
                            url={apiUrls['companies']}
                            search_text="production companies"
                            callback={(response) => response.data}
                            invalid={invalid}
                        />}
                    />
                    {/*If user creates an option, value and label are both the input string*/}
                </Form.Group>
            </Row>
            <Row>
                <Form.Group className="mb-3" controlId="network">
                    <Form.Label id="network-label">Network or streaming platform</Form.Label>
                    <Controller
                        name='network'
                        control={control}
                        render={({   field ,
                                     fieldState: { invalid }}) =>
                        <AsyncAPISelect
                            ariaLabelledby="network-label"
                            {...field}
                            lsmValue={state.formData.network}
                            creatable={true}
                            isMulti={false}
                            url={apiUrls['networks']}
                            search_text="a network or streaming platform"
                            callback={(response) => response.data}
                            invalid={invalid}
                        />}
                    />
                </Form.Group>
            </Row>

            <Row>
                <Col xs={6}>
                    <Form.Group className="mb-3" controlId="genre">
                        <Form.Label id="genre-label">Genre</Form.Label>
                        <Controller
                            name='genre'
                            data-testid='genre-select'
                            control={control}
                            render={({   field ,
                                         fieldState: { invalid }}) =>
                            <Select
                                isClearable
                                aria-labelledby="genre-label"
                                {...field}
                                options={genreOptions}
                                placeholder={''}
                                styles={customStyles(invalid)}
                            />}
                        />
                    </Form.Group>
                </Col>
                <Col xs={6}>
                    <Form.Group className="mb-3" controlId="union">
                        <Form.Label id="union-label">Union status</Form.Label>
                        <Controller
                            name='union'
                            control={control}
                            render={({   field ,
                                         fieldState: { invalid }}) =>
                            <Select
                                isClearable
                                aria-labelledby="union-label"
                                {...field}
                                options={unionOptions}
                                placeholder={''}
                                styles={customStyles(invalid)}
                            />}
                        />
                    </Form.Group>
                </Col>
            </Row>

            <Row>
                <Form.Group className="mb-3" controlId="locations">
                    <Form.Label id="locations-label">Filming locations</Form.Label>
                    <Controller
                        name='locations'
                        control={control}
                        render={({   field ,
                                     fieldState: { invalid }}) =>
                        <AsyncAPISelect
                            ariaLabelledby="locations-label"
                            {...field}
                            lsmValue={state.formData.locations}
                            creatable={false}
                            isMulti={true}
                            url={apiUrls['autocomplete']}
                            search_text="filming locations"
                            callback={
                                (response) => response.data['predictions'].map(prediction => ({
                                    value: prediction['place_id'],
                                    label: prediction['description'],
                                }))
                            }
                            invalid={invalid}
                            onChange={
                                (inputValue, action) => {
                                    field.onChange(inputValue, action);
                                    handleLocationChange(inputValue, action);
                                }
                            }
                            getSessionToken={getSessionToken}
                        />}
                    />
                </Form.Group>
            </Row>

                {/*Selected option list is state.selectValue*/}
                {/*selectValue is always a list, even if the select element is not multiple*/}

            <Row className="mt-3">
                <Col xs={9}>
                </Col>
                <Col xs={3}>
                    <Row className="mx-0">
                        <Button type="submit" size="sm">Next</Button>
                    </Row>

                </Col>
            </Row>
            </Form>
        </div>
    )
}

export default PageOne;