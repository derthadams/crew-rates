import { dataDefault } from "./Survey";

export function updateLocationDetails(state, payload) {
    return {
        ...state,
        locationDetails: {
            ...state.locationDetails,
            [payload.key]: payload.value,
        }
    }
}

export function updateFormData(state, payload) {
    return {
        ...state,
        formData: {
            ...state.formData,
            ...payload,
        }
    }
}

export function clearFormData() {
    return dataDefault;
}