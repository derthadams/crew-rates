import {
    BRRender as render,
    screen,
} from "./test-utils/testing-library-utils";
import "@testing-library/jest-dom";

import { dataDefault as mockDataDefault } from "../src/add-rate/dataDefault";

import optionsScript from "./optionsScript";

import { server } from "./mocks/server";
import Failure from "../src/add-rate/Failure";


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

describe("Failure page", () => {
    test('Failure page renders', () => {
        render(<Failure />)
        const failureHeader = screen.getByText(/oops!/i)
        expect(failureHeader).toBeInTheDocument();
    })
})