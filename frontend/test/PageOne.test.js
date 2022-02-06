import {
    BRRender as render,
    screen,
    waitFor,
} from "./test-utils/testing-library-utils";
import selectEvent from "react-select-event";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import PageOne from "../src/PageOne";
import { dataDefault as mockDataDefault } from "../src/dataDefault";

import optionsScript from "./optionsScript";

import { server } from "./mocks/server";


const mockedUsedNavigate = jest.fn();
jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useNavigate: () => mockedUsedNavigate,
}));

jest.mock("little-state-machine", () => ({
    useStateMachine: () => {
        return {
            actions: {
                updateFormData: jest.fn(),
                updateLocationDetails: jest.fn(),
            },
            state: mockDataDefault,
        };
    },
    createStore: jest.fn(),
}));

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

describe("PageOne create options in fields", () => {
    test("Create show", async () => {
        render(<PageOne />);
        const form = screen.getByRole("form");

        const show = screen.getByLabelText(/show title/i);
        await selectEvent.create(show, "An Unknown Show");

        const season = screen.getByLabelText(/season/i);
        userEvent.type(season, "1");
        expect(form).toHaveFormValues({ season_number: 1 });

        const startDate = screen.getByLabelText(/start date/i);
        userEvent.type(startDate, "2022-02-02");
        expect(form).toHaveFormValues({ start_date: "2022-02-02" });

        const nextButton = screen.getByRole("button", { name: /next/i });
        expect(nextButton).toBeInTheDocument();
        userEvent.click(nextButton);

        await waitFor(() =>
            expect(mockedUsedNavigate).toHaveBeenCalledWith(`/2`, {
                state: { fromForm: true },
            })
        );
    });
});

describe("PageOne form validation", () => {
    test("show required validation", async () => {
        render(<PageOne />);

        // User enters season and start date but no show title
        const season = screen.getByLabelText(/season/i);
        userEvent.type(season, "5");

        const startDate = screen.getByLabelText(/start date/i);
        userEvent.type(startDate, "2022-02-02");

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        const showError = await screen.findByText(/show title is required/i);
        expect(showError).toBeInTheDocument();

        const seasonError = screen.queryByText(/season is required/i);
        expect(seasonError).not.toBeInTheDocument();

        const startDateError = screen.queryByText(/start date is required/i);
        expect(startDateError).not.toBeInTheDocument();
    });

    test("season required validation", async () => {
        render(<PageOne />);

        // User enters show and start date but no season
        const show = screen.getByLabelText(/show title/i);
        userEvent.type(show, "Pro");
        await selectEvent.select(show, "Prop Culture");

        const startDate = screen.getByLabelText(/start date/i);
        userEvent.type(startDate, "2022-02-02");

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        await waitFor(() =>
            expect(
                screen.queryByText(/show title is required/i)
            ).not.toBeInTheDocument()
        );

        const seasonError = screen.queryByText(/season is required/i);
        expect(seasonError).toBeInTheDocument();

        const startDateError = screen.queryByText(/start date is required/i);
        expect(startDateError).not.toBeInTheDocument();
    });

    test("season required validation when user backspace deletes their entry", async () => {
        render(<PageOne />);

        // User enters show, enters a season and backspaces out of it, enters start date
        const show = screen.getByLabelText(/show title/i);
        userEvent.type(show, "Pro");
        await selectEvent.select(show, "Project Runway");

        const season = screen.getByLabelText(/season/i);
        userEvent.type(season, "5");
        userEvent.type(season, "{Backspace}");

        const startDate = screen.getByLabelText(/start date/i);
        userEvent.type(startDate, "2022-02-02");

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        await waitFor(() =>
            expect(
                screen.queryByText(/show title is required/i)
            ).not.toBeInTheDocument()
        );

        const seasonError = screen.queryByText(/season is required/i);
        expect(seasonError).toBeInTheDocument();

        const startDateError = screen.queryByText(/start date is required/i);
        expect(startDateError).not.toBeInTheDocument();
    });

    test("start_date required validation", async () => {
        render(<PageOne />);

        // User enters show and season but no start date
        const show = screen.getByLabelText(/show title/i);
        userEvent.type(show, "Pro");
        await selectEvent.select(show, "Prop Culture");

        const season = screen.getByLabelText(/season/i);
        userEvent.type(season, "5");

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        await waitFor(() =>
            expect(
                screen.queryByText(/show title is required/i)
            ).not.toBeInTheDocument()
        );

        const seasonError = screen.queryByText(/season is required/i);
        expect(seasonError).not.toBeInTheDocument();

        const startDateError = screen.queryByText(/start date is required/i);
        expect(startDateError).toBeInTheDocument();
    });

    test("end date is equal to start date", async () => {
        render(<PageOne />);

        const show = screen.getByLabelText(/show title/i);
        userEvent.type(show, "Pro");
        await selectEvent.select(show, "Prop Culture");

        const season = screen.getByLabelText(/season/i);
        userEvent.type(season, "5");

        const startDate = screen.getByLabelText(/start date/i);
        userEvent.type(startDate, "2022-02-02");

        const endDate = screen.getByLabelText(/end date/i);
        userEvent.type(endDate, "2022-02-02");

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        await waitFor(() =>
            expect(mockedUsedNavigate).toHaveBeenCalledWith(`/2`, {
                state: { fromForm: true },
            })
        );
    });

    test("end date is before start date", async () => {
        render(<PageOne />);

        const show = screen.getByLabelText(/show title/i);
        userEvent.type(show, "Pro");
        await selectEvent.select(show, "Prop Culture");

        const season = screen.getByLabelText(/season/i);
        userEvent.type(season, "5");

        const startDate = screen.getByLabelText(/start date/i);
        userEvent.type(startDate, "2022-02-02");

        const endDate = screen.getByLabelText(/end date/i);
        userEvent.type(endDate, "2022-01-02");

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        const startDateError = await screen.findByText(
            /end date should be later than start date/i
        );
        expect(startDateError).toBeInTheDocument();
    });
});

describe("PageOne happy path", () => {
    test("happy path", async () => {
        render(<PageOne />);
        // User fills in all fields
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

        const companies = screen.getByLabelText(/production companies/i);
        userEvent.type(companies, "End");
        await selectEvent.select(companies, "EndemolShine NorthAmerica");

        const network = screen.getByLabelText(/network or streaming platform/i);
        userEvent.type(network, "Dis");
        await selectEvent.select(network, "Disney+");

        const genre = screen.getByLabelText(/genre/i);
        await selectEvent.select(genre, "Reality");
        expect(form).toHaveFormValues({ genre: "RE" });

        const union = screen.getByLabelText(/union status/i);
        await selectEvent.select(union, "IATSE");
        expect(form).toHaveFormValues({ union: "IA" });

        const locations = screen.getByLabelText(/filming locations/i);
        userEvent.type(locations, "Bur");
        await selectEvent.select(locations, "Burbank, CA, USA");

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        await waitFor(() =>
            expect(mockedUsedNavigate).toHaveBeenCalledWith(`/2`, {
                state: { fromForm: true },
            })
        );
    });
});
