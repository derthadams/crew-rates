valid_json = {
    "show": '48a6f024-2aa1-4f29-8db0-de0454385a2c',
    "show_title": "Project Runway",
    "season_number": 4,
    "companies": [
        {
            "uuid": "0fa1f64b-58d6-4963-914c-b0711c70e051",
            "name": "Magical Elves"
        }
    ],
    "network": 'a7f641e0-bbfc-4469-9acd-404f2c8b923f',
    "network_name": "Bravo",
    "genre": "RE",
    "union": "IA",
    "locations": [
        {
            "display_name": "Los Angeles, CA, USA",
            "latitude": "34.0522342",
            "longitude": "-118.2436849",
            "scopes": [
                {
                    "long_name": "Los Angeles",
                    "short_name": "Los Angeles",
                    "type": "locality",
                    "display_name": "Los Angeles, CA, US"
                },
                {
                    "long_name": "Los Angeles County",
                    "short_name": "Los Angeles County",
                    "type": "administrative_area_level_2",
                    "display_name": "Los Angeles County, CA, US"
                },
                {
                    "long_name": "California",
                    "short_name": "CA",
                    "type": "administrative_area_level_1",
                    "display_name": "California, US"
                },
                {
                    "long_name": "United States",
                    "short_name": "US",
                    "type": "country",
                    "display_name": "United States"
                }
            ]
        }
    ],
    "start_date": "2022-01-01",
    "end_date": "2022-01-31",
    "job_title": "5c09a673-d0c7-481f-8500-36c581bd7b4e",
    "job_title_name": "Camera Operator",
    "offered_hourly": 50,
    "offered_guarantee": 12,
    "negotiated": True,
    "increased": True,
    "final_hourly": 72.7273,
    "final_guarantee": 10
}

valid_json_create = {
    "show": "00000000-0000-0000-0000-000000000000",
    "show_title": "Project Runway",
    "season_number": 4,
    "companies": [
        {
            "uuid": "00000000-0000-0000-0000-000000000000",
            "name": "Magical Elves"
        }
    ],
    "network": "00000000-0000-0000-0000-000000000000",
    "network_name": "Bravo",
    "genre": "RE",
    "union": "IA",
    "locations": [
        {
            "display_name": "Los Angeles, CA, USA",
            "latitude": "34.0522342",
            "longitude": "-118.2436849",
            "scopes": [
                {
                    "long_name": "Los Angeles",
                    "short_name": "Los Angeles",
                    "type": "locality",
                    "display_name": "Los Angeles, CA, US"
                },
                {
                    "long_name": "Los Angeles County",
                    "short_name": "Los Angeles County",
                    "type": "administrative_area_level_2",
                    "display_name": "Los Angeles County, CA, US"
                },
                {
                    "long_name": "California",
                    "short_name": "CA",
                    "type": "administrative_area_level_1",
                    "display_name": "California, US"
                },
                {
                    "long_name": "United States",
                    "short_name": "US",
                    "type": "country",
                    "display_name": "United States"
                }
            ]
        }
    ],
    "start_date": "2022-01-01",
    "end_date": "2022-01-31",
    "job_title": "00000000-0000-0000-0000-000000000000",
    "job_title_name": "Camera Operator",
    "offered_hourly": 50,
    "offered_guarantee": 12,
    "negotiated": False,
    "increased": "",
    "final_hourly": None,
    "final_guarantee": None
}

valid_json_no_locations = {  # noqa
    "job_title": "00000000-0000-0000-0000-000000000000",
    "job_title_name": "Camera Operator",
    "offered_hourly": 54.5454,
    "offered_guarantee": 10,
    "show": "00000000-0000-0000-0000-000000000000",
    "show_title": "Project Runway",
    "season_number": 4,
    "companies": [{"uuid": "00000000-0000-0000-0000-000000000000",
                   "name": "Magical Elves"}],
    "network": '00000000-0000-0000-0000-000000000000',
    "network_name": "Bravo",
    "locations": [],
    "start_date": "2021-01-01",
    "end_date": "2021-02-01",
    "union": "IA",
    "genre": "RE",
    "negotiated": False
}