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

    test("enter daily, negotiated true increase true, enter final", async () => {
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

    test("clear zero day rate when click to hourly with no guarantee", () => {
        render(<PageTwo />);

        const form = screen.getByRole("form");
        const offeredDayRate = screen.getByRole("spinbutton", {
            name: "offered_day_rate",
        });
        userEvent.type(offeredDayRate, "0");
        expect(form).toHaveFormValues({ offered_day_rate: 0 });

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
    });

    test("clear zero hourly rate when click to day rate with no guarantee", () => {
        render(<PageTwo />);

        const form = screen.getByRole("form");
        const offeredHourly = screen.getByRole("spinbutton", {
            name: "offered_hourly_rate",
        });
        userEvent.type(offeredHourly, "0");
        expect(form).toHaveFormValues({ offered_hourly_rate: 0 });

        const offeredDayRate = screen.getByRole("spinbutton", {
            name: "offered_day_rate",
        });
        userEvent.click(offeredDayRate);
        expect(form).toHaveFormValues({ offered_hourly_rate: null });
    });

    // User tries to advance without entering an offered rate
    // - entering daily but not guarantee
    test("user tries to advance with only job title and offered daily", async () => {
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

        const guaranteeError = await screen.findByText(
            /guarantee is required/i
        );
        expect(guaranteeError).toBeInTheDocument();

        const hourlyError = screen.queryByText(/hourly rate is required/i);
        expect(hourlyError).toBeInTheDocument();

        const negotiatedError = screen.queryByText(
            /this question is required/i
        );
        expect(negotiatedError).toBeInTheDocument();

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledTimes(0);
        });
    });
    // - entering hourly but not guarantee
    test("user tries to advance with only job title and offered hourly", async () => {
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

        const guaranteeError = await screen.findByText(
            /guarantee is required/i
        );
        expect(guaranteeError).toBeInTheDocument();

        const dayRateError = screen.queryByText(/day rate is required/i);
        expect(dayRateError).toBeInTheDocument();

        const negotiatedError = screen.queryByText(
            /this question is required/i
        );
        expect(negotiatedError).toBeInTheDocument();

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledTimes(0);
        });
    });
    // - entering neither hourly nor daily
    test("user tries to advance with only job title", async () => {
        render(<PageTwo />);

        const jobTitle = screen.getByLabelText(
            /what was your job title on the show?/i
        );
        userEvent.type(jobTitle, "Cam");
        await selectEvent.select(jobTitle, "Camera Assistant");

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        const guaranteeError = await screen.findByText(
            /guarantee is required/i
        );
        expect(guaranteeError).toBeInTheDocument();

        const dayRateError = screen.queryByText(/day rate is required/i);
        expect(dayRateError).toBeInTheDocument();

        const negotiatedError = screen.queryByText(
            /this question is required/i
        );
        expect(negotiatedError).toBeInTheDocument();

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledTimes(0);
        });
    });
    // User tries to advance without filling any fields
    test("user tries to advance without filling in any fields", async () => {
        render(<PageTwo />);
        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        const jobTitleError = await screen.findByText(/job title is required/i);
        expect(jobTitleError).toBeInTheDocument();

        const guaranteeError = screen.queryByText(/guarantee is required/i);
        expect(guaranteeError).toBeInTheDocument();

        const dayRateError = screen.queryByText(/day rate is required/i);
        expect(dayRateError).toBeInTheDocument();

        const negotiatedError = screen.queryByText(
            /this question is required/i
        );
        expect(negotiatedError).toBeInTheDocument();

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledTimes(0);
        });
    });

    // User enters job title and offered rate, tries to advance without answering negotiated
    test("user enters job title and offered rate but not negotiated", async () => {
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

        const offeredGuarantee = screen.getByRole("spinbutton", {
            name: "offered_guarantee",
        });
        userEvent.type(offeredGuarantee, "10");

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        const negotiatedError = await screen.findByText(
            /this question is required/i
        );
        expect(negotiatedError).toBeInTheDocument();

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledTimes(0);
        });
    });

    // User enters job title, offered rate, and negotiated but doesn't answer increased
    test("user enters job title, offered rate, negotiated, but not increased", async () => {
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

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        const increasedError = await screen.findByText(
            /this question is required/i
        );
        expect(increasedError).toBeInTheDocument();

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledTimes(0);
        });
    });

    // User selects negotiated and increased but doesn't enter a final rate
    // - entering daily but not guarantee
    test("user enters job title, offered, negotiated, increased, only daily", async () => {
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

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        const guaranteeError = await screen.findByText(
            /guarantee is required/i
        );
        expect(guaranteeError).toBeInTheDocument();

        const dayRateError = screen.queryByText(/day rate is required/i);
        expect(dayRateError).not.toBeInTheDocument();

        const hourlyRateError = screen.queryByText(/hourly rate is required/i);
        expect(hourlyRateError).toBeInTheDocument();

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledTimes(0);
        });
    });
    // - entering hourly but not guarantee
    test("user enters job title, offered, negotiated, increased, only hourly", async () => {
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

        const finalHourlyRate = screen.getByRole("spinbutton", {
            name: "final_hourly_rate",
        });
        userEvent.type(finalHourlyRate, "80");

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        const guaranteeError = await screen.findByText(
            /guarantee is required/i
        );
        expect(guaranteeError).toBeInTheDocument();

        const dayRateError = screen.queryByText(/day rate is required/i);
        expect(dayRateError).toBeInTheDocument();

        const hourlyRateError = screen.queryByText(/hourly rate is required/i);
        expect(hourlyRateError).not.toBeInTheDocument();

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledTimes(0);
        });
    });
    // - entering neither hourly nor daily
    test("user enters job title, offered, negotiated, increased, but no final", async () => {
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

        const nextButton = screen.getByRole("button", { name: /next/i });
        userEvent.click(nextButton);

        const dayRateError = await screen.findByText(/day rate is required/i);
        expect(dayRateError).toBeInTheDocument();

        const guaranteeError = screen.queryByText(/guarantee is required/i);
        expect(guaranteeError).toBeInTheDocument();

        const hourlyRateError = screen.queryByText(/hourly rate is required/i);
        expect(hourlyRateError).toBeInTheDocument();

        await waitFor(() => {
            expect(mockedUsedNavigate).toHaveBeenCalledTimes(0);
        });
    });

    // User enters number then backspace-deletes their number - check that counterpart number
    // has an emptystring/null value in input (not 0)
    // - for daily
    test("user enters daily and guarantee, backspaces out daily", async () => {
        render(<PageTwo />);

        const form = screen.getByRole("form");

        const offeredDayRate = screen.getByRole("spinbutton", {
            name: "offered_day_rate",
        });
        userEvent.type(offeredDayRate, "650");

        const offeredGuarantee = screen.getByRole("spinbutton", {
            name: "offered_guarantee",
        });
        userEvent.type(offeredGuarantee, "10");
        expect(form).toHaveFormValues({ offered_hourly_rate: 59.0909 });

        userEvent.type(offeredDayRate, "{Backspace}{Backspace}{Backspace}");
        const offeredHourlyRate = screen.getByRole("spinbutton", {
            name: "offered_hourly_rate",
        });

        expect(offeredHourlyRate).toHaveValue(null);
    });
    // - for guarantee
    test("user enters hourly and guarantee, backspaces out guarantee", async () => {
        render(<PageTwo />);

        const form = screen.getByRole("form");

        const offeredHourlyRate = screen.getByRole("spinbutton", {
            name: "offered_hourly_rate",
        });
        userEvent.type(offeredHourlyRate, "70");

        const offeredGuarantee = screen.getByRole("spinbutton", {
            name: "offered_guarantee",
        });
        userEvent.type(offeredGuarantee, "10");
        expect(form).toHaveFormValues({ offered_day_rate: 770 });

        userEvent.type(offeredGuarantee, "{Backspace}{Backspace}");
        const offeredDayRate = screen.getByRole("spinbutton", {
            name: "offered_day_rate",
        });

        expect(offeredDayRate).toHaveValue(null);
    });
    // - for hourly
    test("user enters hourly and guarantee, backspaces out hourly", async () => {
        render(<PageTwo />);

        const form = screen.getByRole("form");

        const offeredHourlyRate = screen.getByRole("spinbutton", {
            name: "offered_hourly_rate",
        });
        userEvent.type(offeredHourlyRate, "70");

        const offeredGuarantee = screen.getByRole("spinbutton", {
            name: "offered_guarantee",
        });
        userEvent.type(offeredGuarantee, "10");
        expect(form).toHaveFormValues({ offered_day_rate: 770 });

        userEvent.type(offeredHourlyRate, "{Backspace}{Backspace}");
        const offeredDayRate = screen.getByRole("spinbutton", {
            name: "offered_day_rate",
        });

        expect(offeredDayRate).toHaveValue(null);
    });

    // If user enters value in a rateWidget field, then backspaces it out, check that it's null
    // - daily
    test("user enters daily and backspaces it out", async () => {
        render(<PageTwo />);

        const offeredDayRate = screen.getByRole("spinbutton", {
            name: "offered_day_rate",
        });
        userEvent.type(offeredDayRate, "650");
        userEvent.type(offeredDayRate, "{Backspace}{Backspace}{Backspace}");
        expect(offeredDayRate).toHaveValue(null);
    });
    // - guarantee
    test("user enters guarantee and backspaces it out", async () => {
        render(<PageTwo />);

        const offeredGuarantee = screen.getByRole("spinbutton", {
            name: "offered_guarantee",
        });
        userEvent.type(offeredGuarantee, "12");
        userEvent.type(offeredGuarantee, "{Backspace}{Backspace}{Backspace}");
        expect(offeredGuarantee).toHaveValue(null);
    });
    // - hourly
    test("user enters hourly and backspaces it out", async () => {
        render(<PageTwo />);

        const offeredHourlyRate = screen.getByRole("spinbutton", {
            name: "offered_hourly_rate",
        });
        userEvent.type(offeredHourlyRate, "59.0909");
        userEvent.type(
            offeredHourlyRate,
            "{Backspace}{Backspace}{Backspace}{Backspace}{Backspace}{Backspace}{Backspace}{Backspace}{Backspace}"
        );
        expect(offeredHourlyRate).toHaveValue(null);
    });

    // If user submits with 0 in day rate, check for error
    // If user submits with 0 in guarantee, check for error
    // If user submits with 0 in hourly rate, check for error

    // User expands form to "did you get...", then changes negotiated to no - form retracts to negotiated
    // User expands form all the way, then changes negotiated to no - form retracts to negotiated
    // User expands form all the way, then changes increased to no - form retracts to increased
});
