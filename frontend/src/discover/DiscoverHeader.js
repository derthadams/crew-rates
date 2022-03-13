import React from "react";

import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import Row from "react-bootstrap/Row";

import AsyncSelect from "react-select/async";

import axios from 'axios';

import "./discover-header.css";

const MINIMUM_QUERY_LENGTH = 2;

const badgeColors = {
    "Show": "primary",
    "Job Title": "success",
    "Company": "dark",
    "Network": "secondary"
}

export default function DiscoverHeader ({ genreOptions, unionOptions,
                                            dateRange, handleDateChange,
                                            unionSelect, handleUnionChange,
                                            genreSelect, handleGenreChange,
                                            handleFilterChange,
                                            searchURL}) {
    const asyncOptions = (inputValue) =>
        inputValue.length >= MINIMUM_QUERY_LENGTH &&
        axios.get(searchURL, { params:{ q: inputValue }})
                .then((response) => response.data)


    const formatLabel = (option) => {
        const optionHTML = `<span>${option.label}</span>
                            <span class="badge rounded-pill p-1 mt-1 mb-1 
                                         bg-${badgeColors[option.type]}">
                                <small>${option.type}</small>
                            </span>`

        return (
            <span dangerouslySetInnerHTML={{ __html: optionHTML}}
                  className={"option-container"}
            />
        )
    }

    return (
        <div className={"sticky-top header-wrapper"}>
            <div className={"bg-light pt-1 pb-2"}>
                <div className="">
                    <Row className={"discover-nav-row"}>
                        <Col md={6}>
                            <AsyncSelect
                                components={{dropdownIndicator: null}}
                                formatOptionLabel={formatLabel}
                                isClearable
                                loadOptions={asyncOptions}
                                onChange={handleFilterChange}
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