import { render, screen } from "@testing-library/react";
import '@testing-library/jest-dom';
import Survey from '../src/Survey'
import optionsScript from "./optionsScript";

describe('Survey', () => {
    test('survey is rendering', () => {
        window.history.pushState({}, 'Add a rate', '/add-rate/')
        document.body.innerHTML = optionsScript;

        render(<Survey/>);
        const unionLabel = screen.getByLabelText(/Union status/i);
        expect(unionLabel).toBeEnabled();
    })
})
