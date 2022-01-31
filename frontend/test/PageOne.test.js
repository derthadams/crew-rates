import { render, screen } from "@testing-library/react";
import selectEvent from "react-select-event";
import '@testing-library/jest-dom';

import { StateMachineProvider, createStore } from "little-state-machine";
import { BrowserRouter } from "react-router-dom";

import PageOne from "../src/PageOne"
import {dataDefault} from "../src/Survey";

import optionsScript from "./optionsScript";

test("Page one is rendering", async () => {
    document.body.innerHTML = optionsScript;

    createStore(dataDefault, {});
    render(<StateMachineProvider>
                <BrowserRouter>
                    <PageOne/>
                </BrowserRouter>
            </StateMachineProvider>);

    const form = screen.getByTestId(/page-one-form/i);

    const show = screen.getByLabelText(/show title/i);
    expect(show).toBeEnabled();

    const season = screen.getByLabelText(/season/i);
    expect(season).toBeEnabled();

    const startDate = screen.getByLabelText(/start date/i);
    expect(startDate).toBeEnabled();

    const endDate = screen.getByLabelText(/start date/i);
    expect(endDate).toBeEnabled();

    const companies = screen.getByLabelText(/production companies/i);
    expect(companies).toBeEnabled();

    const network = screen.getByLabelText(/network or streaming platform/i);
    expect(network).toBeEnabled();

    const genre = screen.getByLabelText(/genre/i);
    await selectEvent.select(genre, "Reality");
    expect(form).toHaveFormValues({genre: "RE"});

    const union = screen.getByLabelText(/union status/i);
    await selectEvent.select(union, "IATSE");
    expect(form).toHaveFormValues({union: "IA"});

    const locations = screen.getByLabelText(/filming locations/i);
    expect(locations).toBeEnabled();
})