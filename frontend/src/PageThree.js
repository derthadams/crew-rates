import React, { useState } from 'react';

import { useNavigate } from "react-router-dom";

import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import Table from "react-bootstrap/Table"
import Card from "react-bootstrap/Card"

import { useStateMachine } from "little-state-machine";
import ProgressBar from "react-bootstrap/ProgressBar";
import Button from "react-bootstrap/Button";

import {NIL as uuid_NIL} from "uuid";

import axios from 'axios'

import {BASE_URL} from "./Survey";

function PageThree(props) {
    const {state} = useStateMachine();
    let navigate = useNavigate();

    const handleSubmit = () => {
        const formData = state.formData;
        let selected_location_details = [];
        for(let location of formData.locations) {
            selected_location_details.push(state.locationDetails[location.value]);
        }

        let data = {
            show: formData.show_title.value === formData.show_title.label ? uuid_NIL : formData.show_title.value,
            show_title: formData.show_title.label,
            season_number: formData.season_number,
            companies: formData.companies.map((company) => {
                return {
                    uuid: company.value === company.label ? uuid_NIL : company.value,
                    name: company.label}
            }),
            network: formData.network ?
                (formData.network.value === formData.network.label ? uuid_NIL : formData.network.value) :
                '',
            network_name: formData.network ? formData.network.label : '',
            genre: formData.genre ? formData.genre.value : '',
            union: formData.union ? formData.union.value : '',
            locations: selected_location_details,
            start_date: formData.start_date,
            end_date: formData.end_date,
            job_title: formData.job_title.value === formData.job_title.label ? uuid_NIL : formData.job_title.value,
            job_title_name: formData.job_title.label,
            offered_hourly: formData.offered_hourly_rate,
            offered_guarantee: formData.offered_guarantee,
            negotiated: formData.negotiated,
            increased: formData.increased,
            final_hourly: formData.final_hourly_rate || null,
            final_guarantee: formData.final_guarantee || null
        }

        // console.log(data);

        // TODO: Add csrf token to post request
        // ie, axios.post(BASE_URL + 'add-rate/', data, {headers: {"X-CSRFToken": csrftoken}}
        // which is imported as const csrftoken = Cookies.get('csrftoken');

        axios.post(BASE_URL + 'add-rate/', data)
            .then(response => {
                navigate(`/success`)
            })
            .catch((error)=> {
                navigate(`/404`, {state: error.response.data})
        })
    }

    return (
        <div className='my-3'>
            <h1 className="display-1">Add a rate</h1>
            <p>Your anonymous rate information will help all crew members
                negotiate better deals.</p>
            <h6 className="display-6">Review and Submit</h6>
            <ProgressBar now={100} label=" Step 3 of 3" className="mx-6 my-3"/>
            {/*<h1>Page Three</h1>*/}
            <Card>
                <Card.Body>
                    Please review the information you entered. <br/>
                    Select Edit to make changes, or Submit if everything looks good!
                </Card.Body>
            </Card>
            <Table borderless>
                <tbody>
                <tr>
                    <th>Show title: </th>
                    <td>{state.formData.show_title.label}</td>
                </tr>

                <tr>
                    <th>Season number: </th>
                    <td>{state.formData.season_number}</td>
                </tr>

                {state.formData.companies.length > 0 &&
                <tr>
                    {state.formData.companies.length > 1 ?
                        <th>Companies: </th> :
                        <th>Company: </th>}

                    <td>
                        {state.formData.companies.map((company) => (
                            <span key={company.value}>{company.label}<br/></span>
                        ))}
                    </td>
                </tr>}

                {state.formData.network !== '' &&
                <tr>
                    <th>Network: </th>
                    <td>{state.formData.network.label}</td>
                </tr>}

                {state.formData.genre !== '' &&
                <tr>
                    <th>Genre: </th>
                    <td>{state.formData.genre.label}</td>
                </tr>}

                {state.formData.union !== '' &&
                <tr>
                    <th>Union: </th>
                    <td>{state.formData.union.label}</td>
                </tr>}

                {state.formData.locations.length > 0 &&
                <tr>
                    {state.formData.locations.length > 1 ?
                        <th>Locations: </th> :
                        <th>Location: </th>}

                    <td>
                        {state.formData.locations.map((location) => (
                            <span key={location.value}>{location.label}<br/></span>
                        ))}
                    </td>
                </tr>}

                <tr>
                    <th>Start date: </th>
                    <td>{state.formData.start_date}</td>
                </tr>

                {state.formData.end_date &&
                <tr>
                    <th>End date: </th>
                    <td>{state.formData.end_date}</td>
                </tr>}

                <tr>
                    <th>Job title: </th>
                    <td>{state.formData.job_title.label}</td>
                </tr>

                <tr>
                    <th>Offered rate: </th>
                    <td>${state.formData.offered_day_rate}/{state.formData.offered_guarantee}
                        <span> </span>(${state.formData.offered_hourly_rate}/hr)</td>
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

                {state.formData.negotiated &&
                (<tr>
                    <th colSpan={2}>
                        You
                        {state.formData.increased ?
                            <span> got </span> :
                            <span> did not get </span>}
                        a higher rate.
                    </th>
                </tr>)}

                {state.formData.final_hourly_rate &&
                (<tr>
                    <th>Final rate: </th>
                    <td>${state.formData.final_day_rate}/{state.formData.final_guarantee}
                        <span> </span>(${state.formData.final_hourly_rate}/hr)</td>
                </tr>)}

                </tbody>
            </Table>
            <Row className="mt-3">
                <Col xs={6}>
                </Col>
                <Col xs={3}>
                    <Row className="mx-1">
                        <Button
                            size="sm"
                            onClick={()=>{navigate(`/`);}}>Edit</Button>
                    </Row>
                </Col>
                <Col xs={3}>
                    <Row className="mx-1">
                        <Button
                            size="sm"
                            variant="success"
                            onClick={handleSubmit}>Submit</Button>
                    </Row>
                </Col>
            </Row>
        </div>
    )
}

export default PageThree;