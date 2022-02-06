import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";

const browserRouterWrapper = ({ children }) => {
    return <BrowserRouter>{children}</BrowserRouter>;
};

const BRRender = (ui, options) =>
    render(ui, { wrapper: browserRouterWrapper, ...options });

export * from "@testing-library/react";
export { BRRender };
