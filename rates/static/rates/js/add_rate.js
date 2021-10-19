import { RateWidget } from './RateWidget.js';
// import Cookies from 'js-cookie';

let locationDetails = {};
let sessionID = newSessionID();

let show_id;
let job_title_id;
let company_ids = [];
let network_id;

const csrftoken = Cookies.get('csrftoken');

function newSessionID() {
    return uuid.v4();
}

function makeNewOptionID(event) {
    if(event.params.data.id === event.params.data.text) {
        event.params.data.id = -1;
    }
    // console.log(event.params.data);
}

const workedRateContainer = document.getElementById('rate-widget-base');

const workedRate = new RateWidget('worked-rate', workedRateContainer);

$('#id_show_title')
    .select2({
        minimumInputLength: 3,
        // language: {
        //     inputTooShort: args => ""
        // },
        // allowClear: true,
        tags: true,
        // theme: 'bootstrap4',
        ajax: {
            delay: 250,
            url: '/api/shows/',
        },
        createTag: function (params) {
            let term = $.trim(params.term);
            // console.log(term);
            // if (term === '' || $('input.select2-search__field').val().length < 2) {
            //     return null;
            // }
            // console.log($('#select2-id_show_title-container').text());
            // console.log($(''))
            // $('#select2-id_show_title-container').text("");
            return {
                id: term,
                text: term,

            }
        },
    })
    .on('select2:select', event => {
        if (event.params.data.id === event.params.data.text) {
            show_id = -1;
        } else {
            show_id = event.params.data.id;
        }
        // console.log(`Show ID after select event: ${show_id}`)
    });

// $('#select2-id_show_title-container')
//     .on('click', event => {
//         console.log('click');
//     });
//
// $('.select2-selection')
//     .on('click', event => {
//         console.log('select2-selection');
//     });

$('id-genre')
    .select2({
        theme: 'bootstrap4',
    });

$('#id_job_title_name')
    .select2({
        minimumInputLength: 3,
        language: {
            inputTooShort: args => ""
        },
        tags: true,
        ajax: {
            url: '/api/job-titles/',
        }
    })
    .on('select2:select', event => {
        if (event.params.data.id === event.params.data.text) {
            job_title_id = -1;
        } else {
            job_title_id = event.params.data.id;
        }
    });

$('#id_companies')
    .select2({
        placeholder: "Search for companies...",
        minimumInputLength: 3,
        multiple: true,
        language: {
            inputTooShort: args => ""
        },
        // theme: 'bootstrap4',
        ajax: {
            url: '/api/companies/',
        },
    })
    .on('select2:select', (event) => {
        if (event.params.data.id === event.params.data.text) {
            company_ids.push(-1);
        } else {
            company_ids.push(event.params.data.id);
        }
    });

$('#id_network_name')
    .select2({
        minimumInputLength: 3,
        language: {
            inputTooShort: args => ""
        },
        tags: true,
        ajax: {
            url: '/api/networks/',
        }
    })
    .on('select2:select', event => {
        if (event.params.data.id === event.params.data.text) {
            network_id = -1;
        } else {
            network_id = event.params.data.id;
        }
    });

$('#id_locations')
    .select2({
        placeholder: "Search for locations...",
        minimumInputLength: 3,
        multiple: true,
        language: {
            inputTooShort: args => ""
        },
        // theme: 'bootstrap4',
        ajax: {
            url: '/api/autocomplete/',
            data: function(params) {
                return {
                    q: params.term,
                    sessiontoken: sessionID
                };
            },
            processResults: function (json) {
                return {
                    results: $.map(json.predictions, function (item) {
                        return {
                            id: item.place_id,
                            text: item.description
                        }
                    })
                }
            }
        },
    })
    .on('select2:select', (event) => {
        let place_id = event.params.data.id;
        // console.log("sessionID=" + sessionID);
        $.get('/api/details/', {
            q: place_id,
            sessiontoken: sessionID
        })
        .done(result => {
            let scopes = $.map(result.result.address_components, function(item) {
                return {
                    long_name: item.long_name,
                    short_name: item.short_name,
                    type: item.types[0]
                }
            });
            for(let i = 0; i < scopes.length; i++) {
                let display_name = scopes[i].long_name;
                for(let j = i +1; j < scopes.length; j++) {
                    if(scopes[j].type === 'administrative_area_level_1' ||
                    scopes[j].type === 'country') {
                        display_name += ", " + scopes[j].short_name;
                    }
                }
                scopes[i]["display_name"] = display_name;
            }
            locationDetails[place_id] =
                {
                    display_name: result.result.formatted_address,
                    scopes: scopes
                }
        });
        sessionID = newSessionID();
    });

$('#rate-form-submit').on('click', (event) => {
    event.preventDefault();
    let selected_locations = $('#id_locations').select2("data");
    let selected_location_details = [];
    for(let location of selected_locations) {
        selected_location_details.push(locationDetails[location.id])
    }

    const data = {
        job_title: job_title_id || -1,
        job_title_name: $('#id_job_title_name option:selected').text(),
        hourly: Number(workedRate.hourlyRate.toFixed(4)),
        guarantee: workedRate.guaranteedHours,
        show: show_id || -1,
        show_title: $('#id_show_title option:selected').text(),
        season_number: Number($('#id_season_number').val()),
        companies: company_ids,
        network: network_id || -1,
        network_name: $('#id_network_name option:selected').text(),
        locations: selected_location_details,
        start_date: $('#id_start_date').val(),
        end_date: $('#id_end_date').val(),
        union: $('#id_union').val(),
        genre: $('#id_genre').val(),
    };

    $.ajax({
        type: "POST",
        url: "/add-rate/",
        contentType: "application/json; charset=utf-8",
        crossDomain: false,
        dataType: "text",
        async: true,
        data: JSON.stringify(data),
        headers: {
            "X-CSRFToken": csrftoken
        },
        // success: function(result) {
        //     alert(result.Result);
        // }
    });
});