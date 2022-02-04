// import React, {useState} from 'react';
// import {dataDefault} from "../../src/Survey";
//
// export default function MockStateMachine () {
//     const [state, setState] = useState(dataDefault);
//
//     const updateFormData = (payload) => {
//         setState({
//             ...state,
//             formData: {
//                 ...state.formData,
//                 ...payload,
//             }
//         })
//     };
//
//     const clearFormData = () => {
//         setState(dataDefault);
//     };
//
//     const updateLocationDetails = () => {
//     };
//
//     return {
//         actions: {
//             updateFormData,
//             updateLocationDetails,
//             clearFormData
//         },
//         state
//     }
// }

import {dataDefault} from "../../src/Survey";

export default function MockStateMachine() {
    let state = dataDefault;

    const updateFormData = (payload) => {
        state = {
            ...state,
            formData: {
                ...state.formData,
                ...payload
            }
        }
    };

    const clearFormData = () => {
        state = dataDefault;
    }

    const updateLocationDetails = () => {

    };

    return {
        actions: {
            updateFormData,
            updateLocationDetails,
            clearFormData
        },
        state
    }
}
