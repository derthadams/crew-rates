import { render, screen, waitFor } from "./test-utils/testing-library-utils";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";
import PageThree from "../src/PageThree";
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

// Pass optionsScript to the document body and create LSM store
beforeEach(() => {
    document.body.innerHTML = optionsScript;
});

// Reset any request handlers that we may add during the tests,
// so they don't affect other tests.
afterEach(() => server.resetHandlers());

// Clean up after the tests are finished.
afterAll(() => server.close());

describe("PageThree tests", () => {
    test("Edit button causes redirect to PageOne", async () => {
        render(<PageThree />);

        const editButton = screen.getByRole("button", { name: /edit/i });
        userEvent.click(editButton);

        await waitFor(() =>
            expect(mockedUsedNavigate).toHaveBeenCalledWith(`/`, {
                state: { fromForm: true },
            })
        );
    });
    test("Submit button text changes and causes redirect to Success page", async () => {
        render(<PageThree />);

        const submitButton = screen.getByRole("button", { name: /submit/i });
        userEvent.click(submitButton);

        const sending = await screen.findByText(/sending.../i);
        expect(sending).toBeInTheDocument();

        await waitFor(() =>
            expect(mockedUsedNavigate).toHaveBeenCalledWith(`/success`, {
                state: { fromForm: true },
            })
        );
    });
});
// When user clicks edit, make sure useNavigate is called with page one

// When user clicks submit, make sure button text changes and a call is made to the add-rate API
