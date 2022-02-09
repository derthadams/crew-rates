import React from "react";
import ProgressBar from "react-bootstrap/ProgressBar";

export default function AddRateHeading({ subheading, now, label }) {
    return (
        <div>
            <h1 className="display-1">Add a rate</h1>

            <p>
                Your anonymous rate information will help all crew members
                negotiate better deals.
            </p>

            <h6 className="display-6">{subheading}</h6>

            <ProgressBar now={now} label={label} className="mx-6 my-3" />
        </div>
    );
}
