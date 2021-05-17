import { RateWidget } from './RateWidget.js';

let locationDetails = {};
let sessionID = newSessionID();

function newSessionID() {
    return uuid.v4();
}

const workedRateContainer = document.getElementById('rate-widget-base');

const workedRate = new RateWidget('worked-rate', workedRateContainer);