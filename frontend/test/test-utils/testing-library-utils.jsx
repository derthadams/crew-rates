import { render } from "@testing-library/react";
import {StateMachineProvider} from "little-state-machine";
import {BrowserRouter} from "react-router-dom";

const stateMachineBrowserRouter = ({children}) => {
    return (
            <StateMachineProvider>
                <BrowserRouter>
                    {children}
                </BrowserRouter>
            </StateMachineProvider>
    )
}

const LSMBRRender = (ui, options) =>
        render(ui, {wrapper: stateMachineBrowserRouter, ...options});

export * from '@testing-library/react';
export {LSMBRRender as render}