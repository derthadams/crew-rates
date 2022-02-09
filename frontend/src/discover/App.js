import React from 'react';
import RateReport from './RateReport'
import './app.css'

const data = {
    show_title: "Prop Culture",
    season_number: 1,
    company: "Buena Vista Productions",
    network: "Disney+",
    union_status: "IATSE",
    genre: "Documentary",
    job_title: "Camera Operator",
    day_rate: 800,
    guarantee: 10,
    hourly_rate: 72.73,
    increase: 15
}

export default function App() {
    return (
            <div>
                <h1>Discover Page</h1>
                <RateReport show_title={data.show_title}
                            season_number={data.season_number}
                            company={data.company}
                            network={data.network}
                            union_status={data.union_status}
                            genre={data.genre}
                            job_title={data.job_title}
                            day_rate={data.day_rate}
                            guarantee={data.guarantee}
                            hourly_rate={data.hourly_rate}
                            increase={data.increase}/>
            </div>

    )
}