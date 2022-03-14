import React from 'react';
import { BarElement, CategoryScale, Chart as ChartJS,  LinearScale  } from 'chart.js';
import { Bar } from 'react-chartjs-2';

export default function Histogram ({ histogramData, medianRate, binSize }) {
    const FILL_COLOR = '#AED6F1';
    const ACCENT_COLOR = '#0D6EFD';
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

    const transformData = (data) => {
        const lastIndex = data.length - 1
        const minBin = data[0].bin_floor;
        const maxBin = data[lastIndex].bin_floor;

        let labels = [];
        let dataOut = [];
        let backgroundColor = [];

        let dataIndex = 0;
        for (let bin = minBin; bin <= maxBin; bin += binSize) {
            labels.push(bin);
            if(data[dataIndex].bin_floor === bin) {
                dataOut.push(data[dataIndex].count);
                if(medianRate >= bin && medianRate < bin + binSize) {
                    backgroundColor.push(ACCENT_COLOR);
                } else {
                    backgroundColor.push(FILL_COLOR);
                }
                dataIndex += 1;
            } else {
                dataOut.push(0);
            }
        }

        return {
            labels: labels,
            datasets: [
                {
                    data: dataOut,
                    backgroundColor: backgroundColor
                }
            ]
        }

    }

    const chartData = transformData(histogramData);

    ChartJS.register(BarElement, CategoryScale, LinearScale);

    return (
            <Bar
                    options={options}
                    data={chartData}
                    type={'bar'}
                    height={80}
            />
    )
}