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
    test("enter day rate, negotiated false", async () => {
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

        const higherRate = screen.queryByText("Did you get a higher rate?");
        expect(higherRate).not.toBeInTheDocument();

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledWith(`/3`, {
                state: { fromForm: true },
            });
        });
    });

    test("enter hourly, negotiated false", async () => {
        render(<PageTwo />);

        const form = screen.getByRole("form");

        const jobTitle = screen.getByLabelText(
            /what was your job title on the show?/i
        );
        userEvent.type(jobTitle, "Cam");
        await selectEvent.select(jobTitle, "Camera Operator");

        const offeredHourly = screen.getByRole("spinbutton", {
            name: "offered_hourly_rate",
        });
        userEvent.type(offeredHourly, "95");

        const offeredGuarantee = screen.getByRole("spinbutton", {
            name: "offered_guarantee",
        });
        userEvent.type(offeredGuarantee, "8");

        expect(form).toHaveFormValues({ offered_day_rate: 760 });

        const negotiatedNo = screen.getByRole("button", {
            name: "negotiated_no",
        });
        userEvent.click(negotiatedNo);

        const higherRate = screen.queryByText("Did you get a higher rate?");
        expect(higherRate).not.toBeInTheDocument();

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledWith(`/3`, {
                state: { fromForm: true },
            });
        });
    });

    test("enter daily, negotiated true increase false", async () => {
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

        const higherRate = screen.queryByText("Did you get a higher rate?");
        expect(higherRate).toBeInTheDocument();

        const increasedNo = screen.getByRole("button", {
            name: "increased_no",
        });
        userEvent.click(increasedNo);

        const congratulations = screen.queryByText(/congratulations!.*/i);
        expect(congratulations).not.toBeInTheDocument();

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledWith(`/3`, {
                state: { fromForm: true },
            });
        });
    });

    test("enter daily, negotiated true increase true", async () => {
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

        const higherRate = screen.queryByText("Did you get a higher rate?");
        expect(higherRate).toBeInTheDocument();

        const increasedYes = screen.getByRole("button", {
            name: "increased_yes",
        });
        userEvent.click(increasedYes);

        const congratulations = screen.queryByText(/congratulations!.*/i);
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
    });
});

describe("Page Two form validation", () => {
    // User enters a day rate then clicks to hourly
    // Make sure that day rate is cleared
    test("clear day rate when click to hourly with no guarantee", () => {
        render(<PageTwo />);

        const form = screen.getByRole("form");
        const offeredDayRate = screen.getByRole("spinbutton", {
            name: "offered_day_rate",
        });
        userEvent.type(offeredDayRate, "800");
        expect(form).toHaveFormValues({ offered_day_rate: 800 });

        const offeredHourly = screen.getByRole("spinbutton", {
            name: "offered_hourly_rate",
        });
        userEvent.click(offeredHourly);
        expect(form).toHaveFormValues({ offered_day_rate: null });
    });

    // User enters hourly then clicks to daily
    // Make sure that hourly is cleared
    test("clear hourly rate when click to day rate with no guarantee", () => {
        render(<PageTwo />);

        const form = screen.getByRole("form");
        const offeredHourly = screen.getByRole("spinbutton", {
            name: "offered_hourly_rate",
        });
        userEvent.type(offeredHourly, "95");
        expect(form).toHaveFormValues({ offered_hourly_rate: 95 });

        const offeredDayRate = screen.getByRole("spinbutton", {
            name: "offered_day_rate",
        });
        userEvent.click(offeredDayRate);
        expect(form).toHaveFormValues({ offered_hourly_rate: null });
    })

    // User tries to advance without entering an offered rate
    // - entering daily but not guarantee
    test('user tries to advance with only job title and offered daily', async () => {
        render(<PageTwo />);

        const jobTitle = screen.getByLabelText(
                /what was your job title on the show?/i
        );
        userEvent.type(jobTitle, "Cam");
        await selectEvent.select(jobTitle, "Camera Assistant");

        const offeredDayRate = screen.getByRole("spinbutton", {
            name: "offered_day_rate",
        });
        userEvent.type(offeredDayRate, "700");

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        const guaranteeError = await screen.findByText(/guarantee is required/i);
        expect(guaranteeError).toBeInTheDocument();

        const hourlyError = screen.queryByText(/hourly rate is required/i);
        expect(hourlyError).toBeInTheDocument();

        const negotiatedError = screen.queryByText(/this question is required/i);
        expect(negotiatedError).toBeInTheDocument();

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledTimes(0);
        });
    })
    // - entering hourly but not guarantee
    test('user tries to advance with only job title and offered hourly', async () => {
        render(<PageTwo />);

        const jobTitle = screen.getByLabelText(
                /what was your job title on the show?/i
        );
        userEvent.type(jobTitle, "Cam");
        await selectEvent.select(jobTitle, "Camera Assistant");

        const offeredHourly = screen.getByRole("spinbutton", {
            name: "offered_hourly_rate",
        });
        userEvent.type(offeredHourly, "700");

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        const guaranteeError = await screen.findByText(/guarantee is required/i);
        expect(guaranteeError).toBeInTheDocument();

        const dayRateError = screen.queryByText(/day rate is required/i);
        expect(dayRateError).toBeInTheDocument();

        const negotiatedError = screen.queryByText(/this question is required/i);
        expect(negotiatedError).toBeInTheDocument();

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledTimes(0);
        });
    })
    // - entering neither hourly nor daily

    // User enters job title and offered rate, tries to advance without answering negotiated
    test('user enters job title and offered rate but not negotiated', async () => {
        render(<PageTwo />)

        const jobTitle = screen.getByLabelText(
                /what was your job title on the show?/i
        );
        userEvent.type(jobTitle, "Cam");
        await selectEvent.select(jobTitle, "Camera Assistant");

        const offeredDayRate = screen.getByRole("spinbutton", {
            name: "offered_day_rate",
        });
        userEvent.type(offeredDayRate, "700");

        const offeredGuarantee = screen.getByRole("spinbutton", {
            name: "offered_guarantee",
        });
        userEvent.type(offeredGuarantee, "10");

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        const negotiatedError = await screen.findByText(/this question is required/i);
        expect(negotiatedError).toBeInTheDocument();

        // console.log(negotiatedError);

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledTimes(0);
        });
    })

    // User selects negotiated and increased but doesn't enter a final rate
    // - entering daily but not guarantee
    // - entering hourly but not guarantee
    // - entering neither hourly nor daily

    // User enters number then backspace-deletes their number
    // Check that the value is still emptystring (I think this is the default, not 0)
    // - for daily
    // - for guarantee
    // - for hourly
});
