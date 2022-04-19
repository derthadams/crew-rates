from datetime import date
from dateutil.relativedelta import relativedelta

runway_show = {
    'title': 'Project Runway',
    'uuid': '48a6f024-2aa1-4f29-8db0-de0454385a2c'
}

wipeout_show = {
    'title': 'Wipeout',
    'uuid': '4a72cfed-5ad9-4200-964c-0e62f77882b7'
}

love_is_blind_show = {
    'title': 'Love is Blind',
    'uuid': 'a8119331-ce1f-4b38-b603-ed2844500929'
}

real_housewives_show = {
    'title': 'Real Housewives of Beverly Hills',
    'uuid': '1a2ae161-c4bb-4b8e-968e-f59a6c663541'
}

price_is_right = {
    'name': 'The Price is Right',
    'uuid': '0eb1f64b-35d6-4963-914c-b0719c70e051'
}

magical_elves = {
    'name': 'Magical Elves',
    'uuid': '0fa1f64b-58d6-4963-914c-b0711c70e051'
}

endemol = {
    'name': 'EndemolShine NorthAmerica',
    'uuid': 'caf6966d-a961-4a57-8872-39a4f51ce798'
}

kinetic = {
    'name': 'Kinetic Content',
    'uuid': 'fe2c3243-da84-483b-b9ec-4ce34adcb0ea'
}

evolution = {
    'name': 'Evolution Media',
    'uuid': '81f3c0c4-e020-45ff-94e9-b37ba0e4151b'
}

fremantle = {
    'name': 'Fremantle Media',
    'uuid': '4a6428f7-cacd-4432-adbf-99b3f50f6184'
}

bravo = {
    'name': 'Bravo',
    'uuid': 'a7f641e0-bbfc-4469-9acd-404f2c8b923f'
}

tbs = {
    'name': 'TBS',
    'uuid': '5609fa2a-789e-43e0-80d9-d3cb6e77aed8'
}

netflix = {
    'name': 'Netflix',
    'uuid': '1eadc567-7dc5-49c7-95f0-0bbd18d7eea2'
}

cbs = {
    'name': 'CBS',
    'uuid': 'd4ac9bc2-afef-475e-aea9-444ed279b32c'
}

operator = {
    'title': 'Camera Operator',
    'uuid': '5c09a673-d0c7-481f-8500-36c581bd7b4e'
}

runway_report = {
    "show": '48a6f024-2aa1-4f29-8db0-de0454385a2c',
    "show_title": "Project Runway",
    "season_number": 25,
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
    "locations": [],
    "start_date": date.today() + relativedelta(months=-5),
    "end_date": "",
    "job_title": "5c09a673-d0c7-481f-8500-36c581bd7b4e",
    "job_title_name": "Camera Operator",
    "offered_hourly": 50,
    "offered_guarantee": 12,
    "offered_daily": 700,
    "negotiated": True,
    "increased": True,
    "final_hourly": 72.7273,
    "final_guarantee": 10,
    "final_daily": 800
}

wipeout_report = {
    "show": '4a72cfed-5ad9-4200-964c-0e62f77882b7',
    "show_title": "Wipeout",
    "season_number": 5,
    "companies": [
        {
            "uuid": "caf6966d-a961-4a57-8872-39a4f51ce798",
            "name": "EndemolShine NorthAmerica"
        }
    ],
    "network": '5609fa2a-789e-43e0-80d9-d3cb6e77aed8',
    "network_name": "TBS",
    "genre": "RE",
    "union": "IA",
    "locations": [],
    "start_date": date.today() + relativedelta(months=-5),
    "end_date": "",
    "job_title": "5c09a673-d0c7-481f-8500-36c581bd7b4e",
    "job_title_name": "Camera Operator",
    "offered_hourly": 59.0909,
    "offered_guarantee": 10,
    "offered_daily": 650,
    "negotiated": True,
    "increased": True,
    "final_hourly": 63.6363,
    "final_guarantee": 10,
    "final_daily": 700
}

love_is_blind_report = {
    "show": 'a8119331-ce1f-4b38-b603-ed2844500929',
    "show_title": "Love is Blind",
    "season_number": 1,
    "companies": [
        {
            "uuid": "fe2c3243-da84-483b-b9ec-4ce34adcb0ea",
            "name": "Kinetic Content"
        }
    ],
    "network": '1eadc567-7dc5-49c7-95f0-0bbd18d7eea2',
    "network_name": "Netflix",
    "genre": "RE",
    "union": "IA",
    "locations": [],
    "start_date": date.today() + relativedelta(months=-7),
    "end_date": "",
    "job_title": "5c09a673-d0c7-481f-8500-36c581bd7b4e",
    "job_title_name": "Camera Operator",
    "offered_hourly": 54.75,
    "offered_guarantee": 12,
    "offered_daily": 766.5,
    "negotiated": False,
    "increased": False,
    "final_hourly": 54.75,
    "final_guarantee": 12,
    "final_daily": 766.5
}

real_housewives_report = {
    "show": '1a2ae161-c4bb-4b8e-968e-f59a6c663541',
    "show_title": "Real Housewives of Beverly Hills",
    "season_number": 14,
    "companies": [
        {
            "uuid": "81f3c0c4-e020-45ff-94e9-b37ba0e4151b",
            "name": "Evolution Media"
        }
    ],
    "network": '7f641e0-bbfc-4469-9acd-404f2c8b923f',
    "network_name": "Bravo",
    "genre": "RE",
    "union": "NO",
    "locations": [],
    "start_date": date.today() + relativedelta(months=-5),
    "end_date": "",
    "job_title": "5c09a673-d0c7-481f-8500-36c581bd7b4e",
    "job_title_name": "Camera Operator",
    "offered_hourly": 46.4286,
    "offered_guarantee": 12,
    "offered_daily": 650,
    "negotiated": False,
    "increased": False,
    "final_hourly": 46.4286,
    "final_guarantee": 12,
    "final_daily": 650
}

game_show_report = {
    "show": '0eb1f64b-35d6-4963-914c-b0719c70e051',
    "show_title": "The Price is Right",
    "season_number": 72,
    "companies": [
        {
            "uuid": "4a6428f7-cacd-4432-adbf-99b3f50f6184",
            "name": "Fremantle Media"
        }
    ],
    "network": 'd4ac9bc2-afef-475e-aea9-444ed279b32c',
    "network_name": "CBS",
    "genre": "GA",
    "union": "NA",
    "locations": [],
    "start_date": date.today() + relativedelta(months=-5),
    "end_date": "",
    "job_title": "5c09a673-d0c7-481f-8500-36c581bd7b4e",
    "job_title_name": "Camera Operator",
    "offered_hourly": 46.4286,
    "offered_guarantee": 12,
    "offered_daily": 650,
    "negotiated": False,
    "increased": False,
    "final_hourly": 46.4286,
    "final_guarantee": 12,
    "final_daily": 650
}
