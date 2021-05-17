export class RateWidget {
    constructor(id, element) {
        const rateWidgetTemplate = document.getElementById('rate-widget');
        const clone = rateWidgetTemplate.content.cloneNode(true);
        const parentDiv = clone.querySelector('.rate-widget-container');
        const rateInput = parentDiv.querySelector('.rate-input');
        parentDiv.id = id;
        element.appendChild(clone);

        this.dailyRateDisplay = parentDiv.querySelector('.daily-rate-display');
        this.guarHoursDisplay = parentDiv.querySelector('.guar-hours-display');
        this.hourlyRateDisplay = parentDiv.querySelector('.hourly-rate-display');

        this.hourlyRate = 0;
        this.dailyRate = 0;
        this.guaranteedHours = 0;
        this.rateType = 'day';

        rateInput
            .addEventListener('input', (event) => {
                if (this.rateType === 'day') {
                    this.dailyRate = Number(event.target.value);
                    this.calculateRate();
                } else if (this.rateType === 'hour') {
                    this.hourlyRate = Number(event.target.value);
                    this.calculateRate();
                }
            });

        parentDiv.querySelector('.guar-hours-input')
            .addEventListener('input', (event) => {
                this.guaranteedHours = Number(event.target.value);
                this.calculateRate();
            });

        parentDiv.querySelector('.per-day')
            .addEventListener('click', (event) => {
                if (this.rateType === 'hour') {
                    this.rateType = 'day';
                    if (rateInput.value !== "") {
                        this.dailyRate = Number(rateInput.value);
                        this.hourlyRate = 0;
                        this.calculateRate();
                    }
                }
            });

        parentDiv.querySelector('.per-hour')
            .addEventListener('click', (event) => {
                if (this.rateType === 'day') {
                    this.rateType = 'hour';
                    if (rateInput.value !== "") {
                        this.hourlyRate = Number(rateInput.value);
                        this.dailyRate = 0;
                        this.calculateRate();
                    }
                }
            });
    }

    hoursToStraightTime(hours) {
        if (hours <= 8) {
            return hours;
        } else if (hours > 8 && hours <= 12) {
            return 8 + ((hours - 8) * 1.5);
        } else {
            return 14 + ((hours - 12) * 2);
        }
    }

    calculateRate() {
        if (this.rateType === 'day' && this.dailyRate > 0 && this.guaranteedHours > 0) {
            this.hourlyRate = this.dailyRate / this.hoursToStraightTime(this.guaranteedHours);
        } else if (this.rateType === 'hour' && this.hourlyRate > 0 && this.guaranteedHours > 0) {
            this.dailyRate = Math.ceil(this.hourlyRate * this.hoursToStraightTime(this.guaranteedHours));
        }

        if (this.guaranteedHours === 0) {
            if (this.rateType === 'day') {
                this.hourlyRate = 0;
            } else if (this.rateType === "hour") {
                this.dailyRate = 0;
            }
        }
        this.displayRate()
    }

    displayRate() {
        if (this.guaranteedHours <= 0) {
            this.guarHoursDisplay.innerText = "--";
        } else {
            this.guarHoursDisplay.innerText = this.guaranteedHours;
        }

        if (this.dailyRate <= 0) {
            this.dailyRateDisplay.innerText = "---";
        } else
            this.dailyRateDisplay.innerText = this.dailyRate;

        if (this.hourlyRate <= 0) {
            this.hourlyRateDisplay.innerText = "--.--";
        } else {
            this.hourlyRateDisplay.innerText = this.hourlyRate.toFixed(2);
        }
    }
}
