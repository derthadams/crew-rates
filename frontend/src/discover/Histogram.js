import React from 'react';
import { BarElement, CategoryScale, Chart as ChartJS,  LinearScale  } from 'chart.js';
import { Bar } from 'react-chartjs-2';

export default function Histogram ({ histogram }) {
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

    const transformData = (histogram) => {
        const { bins, bin_size, med } = histogram;
        const lastBinIndex = bins.length - 1
        const minBin = bins[0].bin_floor;
        const maxBin = bins[lastBinIndex].bin_floor;

        let labels = [];
        let dataOut = [];
        let backgroundColor = [];

        let dataIndex = 0;
        for (let bin = minBin; bin <= maxBin; bin += bin_size) {
            labels.push(bin);
            if(bins[dataIndex].bin_floor === bin) {
                dataOut.push(bins[dataIndex].count);
                if(med >= bin && med < bin + bin_size) {
                    backgroundColor.push(ACCENT_COLOR);
                } else {
                    backgroundColor.push(FILL_COLOR);
                }
                dataIndex += 1;
            } else {
                dataOut.push(0);
                backgroundColor.push(FILL_COLOR);
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

    const chartData = transformData(histogram);

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