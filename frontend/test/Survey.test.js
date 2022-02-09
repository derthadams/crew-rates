import { render, screen, prettyDOM, waitFor } from "@testing-library/react";
import selectEvent from "react-select-event";
import '@testing-library/jest-dom';
import userEvent from "@testing-library/user-event";
// import { MemoryRouter } from "react-router-dom";

import Survey from '../src/add-rate/Survey'
import optionsScript from "./optionsScript";

import { server } from "./mocks/server";

beforeAll(() => server.listen());

// Pass optionsScript to the document body
beforeEach(() => {
    document.body.innerHTML = optionsScript;
});

// Reset any request handlers that we may add during the tests,
// so they don't affect other tests.
afterEach(() => server.resetHandlers());

// Clean up after the tests are finished.
afterAll(() => server.close());

describe.skip('Survey', () => {
    test('survey is rendering', () => {
        window.history.pushState({}, 'Add a rate', '/add-rate/')

        render(<Survey/>);
        const unionLabel = screen.getByLabelText(/Union status/i);
        expect(unionLabel).toBeEnabled();
    })
    test('survey happy path, complete flow', async () => {
        window.history.pushState({}, 'Add a rate', '/add-rate/')
        render(<Survey/>)
        server.printHandlers()

        const form = screen.getByRole("form");

        const show = screen.getByLabelText(/show title/i);
        userEvent.type(show, "Pro");
        await selectEvent.select(show, "Project Runway");

        const season = screen.getByLabelText(/season/i);
        userEvent.type(season, "5");
        expect(form).toHaveFormValues({ season_number: 5 });

        const startDate = screen.getByLabelText(/start date/i);
        userEvent.type(startDate, "2022-02-02");

        const endDate = screen.getByLabelText(/end date/i);
        userEvent.type(endDate, "2022-09-02");

        // TODO: The commented-out HTTP calls aren't working for some reason, even though the shows call does work, and this code also works in the context of PageTwo.test

        // const companies = screen.getByLabelText(/production companies/i);
        // server.printHandlers();
        // userEvent.type(companies, "End");
        // await selectEvent.select(companies, "EndemolShine NorthAmerica");

        // const network = screen.getByLabelText(/network or streaming platform/i);
        // userEvent.type(network, "Dis");
        // await selectEvent.select(network, "Disney+");

        const genre = screen.getByLabelText(/genre/i);
        await selectEvent.select(genre, "Reality");
        expect(form).toHaveFormValues({ genre: "RE" });

        const union = screen.getByLabelText(/union status/i);
        await selectEvent.select(union, "IATSE");
        expect(form).toHaveFormValues({ union: "IA" });

        // const locations = screen.getByLabelText(/filming locations/i);
        // userEvent.type(locations, "Bur");
        // await selectEvent.select(locations, "Burbank, CA, USA");

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);
        window.history.pushState({}, 'Add a rate', '/add-rate/2')

        console.log(prettyDOM(form, Infinity))

        const rateHeading = await screen.findByText(/rate information/i)
        expect(rateHeading).toBeInTheDocument();
    })
})
