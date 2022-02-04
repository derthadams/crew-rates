import {
    prettyDOM,
    render,
    screen,
    waitFor,
} from "./test-utils/testing-library-utils";
import selectEvent from "react-select-event";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import PageTwo from "../src/PageTwo";

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
            state: {
                locationDetails: {},
                formData: {
                    show_title: "",
                    season_number: "",
                    companies: [],
                    network: "",
                    genre: "",
                    union: "",
                    locations: [],
                    start_date: "",
                    end_date: "",
                    job_title: "",
                    offered_guarantee: "",
                    offered_day_rate: "",
                    offered_hourly_rate: "",
                    negotiated: "",
                    increased: "",
                    final_guarantee: "",
                    final_day_rate: "",
                    final_hourly_rate: "",
                },
            },
        };
    },
    createStore: jest.fn(),
}));

beforeAll(() => server.listen());

// Pass optionsScript to the document body and create LSM store
beforeEach(() => {
    document.body.innerHTML = optionsScript;
});

// Reset any request handlers that we may add during the tests,
// so they don't affect other tests.
afterEach(() => server.resetHandlers());

// Clean up after the tests are finished.
afterAll(() => server.close());

describe("PageTwo happy path", () => {
    test("enter day rate, no negotiation", async () => {
        render(<PageTwo />);

        const form = screen.getByRole("form");

        const jobTitle = screen.getByLabelText(
            /what was your job title on the show?/i
        );
        userEvent.type(jobTitle, "Cam");
        await selectEvent.select(jobTitle, "Camera Operator");

        const offeredDayRate = screen.getByRole("spinbutton", {
            name: "offered_day_rate",
        });
        userEvent.type(offeredDayRate, "750");

        const offeredGuarantee = screen.getByRole("spinbutton", {
            name: "offered_guarantee",
        });
        userEvent.type(offeredGuarantee, "10");

        // const offeredHourly = screen.getByRole("spinbutton", {name: "offered_hourly_rate"});
        expect(form).toHaveFormValues({ offered_hourly_rate: 68.1818 });

        const negotiatedNo = screen.getByRole("button", {
            name: "negotiated_no",
        });
        userEvent.click(negotiatedNo);

        const higherRate = screen.queryByText("Did you get a higher rate?")
        expect(higherRate).not.toBeInTheDocument();

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledWith(`/3`, {
                state: { fromForm: true },
            });
        });
    });

    test('enter hourly, no negotiation', async () => {
        render(<PageTwo />);

        const form = screen.getByRole("form");

        const jobTitle = screen.getByLabelText(
                /what was your job title on the show?/i
        );
        userEvent.type(jobTitle, "Cam");
        await selectEvent.select(jobTitle, "Camera Operator");

        const offeredHourly = screen.getByRole("spinbutton", {name: "offered_hourly_rate"});
        userEvent.type(offeredHourly, "95")

        const offeredGuarantee = screen.getByRole("spinbutton", {
            name: "offered_guarantee",
        });
        userEvent.type(offeredGuarantee, "8");

        expect(form).toHaveFormValues({ offered_day_rate: 760});

        const negotiatedNo = screen.getByRole("button", {
            name: "negotiated_no",
        });
        userEvent.click(negotiatedNo);

        const higherRate = screen.queryByText("Did you get a higher rate?")
        expect(higherRate).not.toBeInTheDocument();

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledWith(`/3`, {
                state: { fromForm: true },
            });
        });
    });

    test('enter daily, negotiated but no increase', async () => {
        render(<PageTwo />);

        const jobTitle = screen.getByLabelText(
                /what was your job title on the show?/i
        );
        userEvent.type(jobTitle, "Cam");
        await selectEvent.select(jobTitle, "Camera Operator");

        const offeredDayRate = screen.getByRole("spinbutton", {
            name: "offered_day_rate",
        });
        userEvent.type(offeredDayRate, "750");

        const offeredGuarantee = screen.getByRole("spinbutton", {
            name: "offered_guarantee",
        });
        userEvent.type(offeredGuarantee, "10");

        const negotiatedYes = screen.getByRole("button", {
            name: "negotiated_yes",
        });
        userEvent.click(negotiatedYes);

        const higherRate = screen.queryByText("Did you get a higher rate?")
        expect(higherRate).toBeInTheDocument();

        const increasedNo = screen.getByRole("button", {
            name: "increased_no",
        });
        userEvent.click(increasedNo);

        const congratulations = screen.queryByText(/congratulations!.*/i)
        expect(congratulations).not.toBeInTheDocument();

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledWith(`/3`, {
                state: { fromForm: true },
            });
        });
    })

    test('enter daily, negotiated and increase', async () => {
        render(<PageTwo />);

        const form = screen.getByRole("form");

        const jobTitle = screen.getByLabelText(
                /what was your job title on the show?/i
        );
        userEvent.type(jobTitle, "Cam");
        await selectEvent.select(jobTitle, "Camera Operator");

        const offeredDayRate = screen.getByRole("spinbutton", {
            name: "offered_day_rate",
        });
        userEvent.type(offeredDayRate, "650");

        const offeredGuarantee = screen.getByRole("spinbutton", {
            name: "offered_guarantee",
        });
        userEvent.type(offeredGuarantee, "12");
        expect(form).toHaveFormValues({ offered_hourly_rate: 46.4286 });

        const negotiatedYes = screen.getByRole("button", {
            name: "negotiated_yes",
        });
        userEvent.click(negotiatedYes);

        const higherRate = screen.queryByText("Did you get a higher rate?")
        expect(higherRate).toBeInTheDocument();

        const increasedYes = screen.getByRole("button", {
            name: "increased_yes",
        });
        userEvent.click(increasedYes);

        const congratulations = screen.queryByText(/congratulations!.*/i)
        expect(congratulations).toBeInTheDocument();

        const finalDayRate = screen.getByRole("spinbutton", {
            name: "final_day_rate",
        });
        userEvent.type(finalDayRate, "850");

        const finalGuarantee = screen.getByRole("spinbutton", {
            name: "final_guarantee",
        });
        userEvent.type(finalGuarantee, "10");

        expect(form).toHaveFormValues({ final_hourly_rate: 77.2727 });

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledWith(`/3`, {
                state: { fromForm: true },
            });
        });
    })

});

describe.skip('Page Two form validation', () => {
    // User enters a day rate then clicks to hourly
    // Make sure that day rate is cleared

    // User enters hourly then clicks to daily
    // Make sure that hourly is cleared
})
