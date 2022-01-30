import { render, screen } from "@testing-library/react";
import '@testing-library/jest-dom';
import PageOne from "../src/PageOne"

test("Page one is rendering", () => {
    render(<PageOne/>);

    const showSelect = screen.getByLabelText('Show title');
    expect(showSelect).toBeEnabled();
})