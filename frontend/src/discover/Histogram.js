import React from 'react';
import { BarElement, CategoryScale, Chart as ChartJS,  LinearScale  } from 'chart.js';
import { Bar } from 'react-chartjs-2';

export default function Histogram () {
    const FILL_COLOR = '#AED6F1';
    const ACCENT_COLOR = '#0d6efd';
    const options = {
        responsive: true,
        scales: {
            y: {
                display: false,
                grid: {
                    display: false
                },
                ticks: {
                    display: false,

                }
            },
            x: {
                display: true,
                grid: {
                    display: false
                },
                ticks: {
                    display: false
                }
            }
        },
        plugins: {
            tooltip: {
                enabled: false
            }
        }
    }

    const data = {
        labels: [50, 55, 60, 65, 70, 75, 80, 85, 90, 95],
        datasets: [
            {
                data: [25, 8, 11, 0, 7, 0, 0, 5, 3, 4],
                backgroundColor: [FILL_COLOR, ACCENT_COLOR, FILL_COLOR, FILL_COLOR, FILL_COLOR,
                    FILL_COLOR, FILL_COLOR, FILL_COLOR, FILL_COLOR, FILL_COLOR]
            }
        ]
    }

    ChartJS.register(BarElement, CategoryScale, LinearScale);

    return (
            <Bar
                    options={options}
                    data={data}
                    type={'bar'}
                    height={80}
            />
    )
}