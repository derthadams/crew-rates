import React, { useState } from 'react';

import {Navigate, useLocation, useNavigate} from "react-router-dom";

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Table from "react-bootstrap/Table";
import Card from "react-bootstrap/Card";
import Spinner from "react-bootstrap/Spinner";

import { useStateMachine } from "little-state-machine";
import { clearFormData } from "./UpdateFunctions";

import {useForm} from "react-hook-form";

import Button from "react-bootstrap/Button";

import {NIL as uuid_NIL} from "uuid";

import axios from 'axios';
import Cookies from 'cookies-js';
import AddRateHeading from "./AddRateHeading";
import convertDate from "../common/convertDate"
import {dataDefault} from "./dataDefault";

function PageThree() {
    const locationState = useLocation();
    const [submitted, setSubmitted] = useState(false);
    const {actions, state} = useStateMachine({ clearFormData });
    const {reset} = useForm();
    let navigate = useNavigate();
    if( !locationState.state?.fromForm) {
        return <Navigate to="/" replace state={{fromForm: true}}/>
    }

    const csrftoken = Cookies.get('csrftoken');
    const apiUrls = JSON.parse(document.getElementById('apiUrls').textContent);

    const handleSubmit = () => {
        setSubmitted(true);
        const formData = state.formData;
        let selected_location_details = [];
        for(let location of formData.locations) {
            selected_location_details.push(state.locationDetails[location.value]);
        }

        let data = {
            show: formData.show_title.value === formData.show_title.label ? uuid_NIL : formData.show_title.value,
            show_title: formData.show_title.label,
            season_number: parseInt(formData.season_number),
            companies: formData.companies.map((company) => {
                return {
                    uuid: company.value === company.label ? uuid_NIL : company.value,
                    name: company.label}
            }),
            network: formData.network ?
                (formData.network.value === formData.network.label ? uuid_NIL : formData.network.value) :
                null,
            network_name: formData.network ? formData.network.label : null,
            genre: formData.genre ? formData.genre.value : null,
            union: formData.union ? formData.union.value : null,
            locations: selected_location_details,
            start_date: formData.start_date,
            end_date: formData.end_date || null,
            job_title: formData.job_title.value === formData.job_title.label ? uuid_NIL : formData.job_title.value,
            job_title_name: formData.job_title.label,
            offered_daily: formData.offered_day_rate,
            offered_hourly: formData.offered_hourly_rate,
            offered_guarantee: formData.offered_guarantee,
            negotiated: formData.negotiated,
            increased: formData.increased,
            final_daily: formData.final_day_rate || formData.offered_day_rate,
            final_hourly: formData.final_hourly_rate || formData.offered_hourly_rate,
            final_guarantee: formData.final_guarantee || formData.offered_guarantee
        }

        axios.post(apiUrls['add-rate-api'], data,
            {
                headers: {
                    "X-CSRFToken": csrftoken
                }
            })
            .then(response => {
                navigate(`/success`, {state: {fromForm: true}})
            })
            .catch((error)=> {
                navigate(`/404`, {state: {errors: error.response.data, fromForm: true}})
        })
    }

    return (
        <div className=''>
            <AddRateHeading step={3}/>

            {/*<Card>*/}
            {/*    <Card.Body>*/}
            {/*        Please review the information you entered.<br/>*/}
            {/*        Select Edit to make changes, or Submit if everything looks good!*/}
            {/*    </Card.Body>*/}
            {/*</Card>*/}
            <Table borderless>
                <tbody>
                <tr>
                    <th>Show title:</th>
                    <td>{state.formData.show_title.label}</td>
                </tr>

                <tr>
                    <th>Season number:</th>
                    <td>{state.formData.season_number}</td>
                </tr>

                {state.formData.companies.length > 0 ?
                <tr>
                    {state.formData.companies.length > 1 ?
                        <th>Companies:</th> :
                        <th>Company:</th>}

                    <td>
                        {state.formData.companies.map((company) => (
                            <span key={company.value}>{company.label}<br/></span>
                        ))}
                    </td>
                </tr> : null}

                {state.formData.network !== '' ?
                <tr>
                    <th>Network:</th>
                    <td>{state.formData.network.label}</td>
                </tr> : null}

                {state.formData.genre !== '' ?
                <tr>
                    <th>Genre:</th>
                    <td>{state.formData.genre.label}</td>
                </tr> : null}

                {state.formData.union !== '' ?
                <tr>
                    <th>Union:</th>
                    <td>{state.formData.union.label}</td>
                </tr> : null}

                {state.formData.locations.length > 0 &&
                <tr>
                    {state.formData.locations.length > 1 ?
                        <th>Locations:</th> :
                        <th>Location:</th>}

                    <td>
                        {state.formData.locations.map((location) => (
                            <span key={location.value}>{location.label}<br/></span>
                        ))}
                    </td>
                </tr>}

                <tr>
                    <th>Start date:</th>
                    <td>{convertDate(state.formData.start_date)}</td>
                </tr>

                {state.formData.end_date ?
                <tr>
                    <th>End date:</th>
                    <td>{convertDate(state.formData.end_date)}</td>
                </tr> : null}

                <tr>
                    <th>Job title:</th>
                    <td>{state.formData.job_title.label}</td>
                </tr>

                <tr>
                    <th>Offered rate:</th>
                    <td>${state.formData.offered_day_rate}/{state.formData.offered_guarantee}
                        <span>&nbsp;</span>(${state.formData.offered_hourly_rate}/hr)</td>
                </tr>

                <tr>
                    <th colSpan={2}>
                        You
                        {state.formData.negotiated ?
                            <span> tried </span> :
                            <span> did not try </span>}
                        to negotiate a higher rate.
                    </th>
                </tr>

                {state.formData.negotiated ?
                (<tr>
                    <th colSpan={2}>
                        You
                        {state.formData.increased ?
                            <span> got </span> :
                            <span> did not get </span>}
                        a higher rate.
                    </th>
                </tr>) : null}

                {state.formData.increased ?
                (<tr>
                    <th>Final rate:</th>
                    <td>${state.formData.final_day_rate}/{state.formData.final_guarantee}
                        <span></span>(${state.formData.final_hourly_rate}/hr)</td>
                </tr>) : null}

                </tbody>
            </Table>
            <Row className="mt-3">
                <Col xs={4} sm={3}>
                    <Row className="mx-1">
                        <Button
                                size="sm"
                                onClick={()=>{navigate(`/`, {state: {fromForm: true}});}}>Edit</Button>
                    </Row>
                </Col>
                <Col xs={4} sm={3}>
                    <Row className={"mx-0"}>
                        <Button
                                variant={"outline-danger"}
                                size={"sm"}
                                onClick={() => {
                                    actions.clearFormData({})
                                    reset(dataDefault.formData);
                                    navigate(`/`, {state: {fromForm: true}});
                                }}
                        >
                            Cancel
                        </Button>
                    </Row>
                </Col>
                <Col xs={4} sm={3}>
                    <Row className="mx-1">
                        {submitted ?
                            (<Button
                                size="sm"
                                variant="success"
                                disabled>
                                <Spinner
                                    as="span"
                                    animation="border"
                                    size="sm"
                                    role="status"
                                    aria-hidden="true"
                                />
                                <span>&nbsp;&nbsp;Sending...</span>
                            </Button>) :

                            (<Button
                                size="sm"
                                variant="success"
                                onClick={handleSubmit}>Submit
                        </Button>)}
                    </Row>
                </Col>
            </Row>
        </div>
    )
}

export default PageThree;