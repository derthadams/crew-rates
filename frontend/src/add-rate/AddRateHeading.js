import React from "react";

export default function AddRateHeading({ step }) {
    return (
        <div className={"mb-3"}>
            <div className={"d-none d-sm-block"}>
            <h3 className="display-3">Add a rate</h3>
            <p>
                Your anonymous rate information will help all crew members
                negotiate better deals.
            </p>
            </div>
            {/*<div className={"d-flex mt-0 px-1"} style={{justifyContent: "space-between"}}>*/}
            {/*    <span className={step === 1 ? "active-text": "greyed-text"}><small>1. Show info</small></span>*/}
            {/*    <span className={step === 2 ? "active-text": "greyed-text"}><small>2. Job info</small></span>*/}
            {/*    <span className={step === 3 ? "active-text": "greyed-text"}><small>3. Review</small></span>*/}
            {/*</div>*/}
            <div className="">
                <div className="progress">
                    <div className={step !== 1 ? "pb-inactive progress-bar" : "progress-bar"}
                         role="progressbar"
                         style={{width: "33%"}}>
                        Show info
                    </div>
                    <div className={step !== 2 ? "pb-inactive progress-bar" : "progress-bar"}
                         style={{width: "34%"}}>Job info
                    </div>
                    <div className={step !== 3 ? "pb-inactive progress-bar" : "progress-bar"}
                         style={{width: "33%"}}>Submit
                    </div>
                </div>
            </div>

        </div>
    );
}
