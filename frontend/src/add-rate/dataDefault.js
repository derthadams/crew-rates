export const pageOneDefault = {
    show_title: '',
    season_number: '',
    companies: [],
    network: '',
    genre: '',
    union: '',
    locations: [],
    start_date: '',
    end_date: '',
}

export const pageTwoDefault = {
    job_title: '',
    offered_guarantee: '',
    offered_day_rate: '',
    offered_hourly_rate: '',
    negotiated: '',
    increased: '',
    final_guarantee: '',
    final_day_rate: '',
    final_hourly_rate: '',
}

export const dataDefault = {
    locationDetails: {},
    formData: {
        ...pageOneDefault,
        ...pageTwoDefault
    }
}