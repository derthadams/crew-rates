import React , { useState, useEffect } from 'react';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import Card from "react-bootstrap/Card";
import { useFormContext, Controller } from "react-hook-form"
import {ErrorMessage} from "@hookform/error-message";


function RateWidget(props) {
    const { control, setValue, getValues , formState } = useFormContext();
    const [daily, setDaily] = useState(getValues(`${props.name}_day_rate`) || 0);
    const [guarantee, setGuarantee] = useState(getValues(`${props.name}_guarantee`) || 0);
    const [hourly, setHourly] = useState(getValues(`${props.name}_hourly_rate`) || 0);
    const [rateType, setRateType] = useState(1);

    const handleDailyChange = (event) => {
        setDaily(parseFloat(Number(event.target.value).toFixed(2)));
    }

    const handleGuaranteeChange = (event) => {
        setGuarantee(Number(event.target.value));
    }

    const handleHourlyChange = (event) => {
        setHourly(parseFloat(Number(event.target.value).toFixed(4)));
    }

    const handleHourlyClick = (event) => {
        setRateType(0);
        if(guarantee === 0 && daily > 0) {
            setDaily(0);
            setValue(`${props.name}_day_rate`, '');
        }
    }

    const handleDailyClick = (event) => {
        setRateType(1);
        if(guarantee === 0 && hourly > 0) {
            setHourly(0);
            setValue(`${props.name}_hourly_rate`, '');
        }
    }

    const recalculateOnDailyChange = () => {
        if (guarantee > 0 && rateType === 1) {
            calculateHourly();
        }
    }

    const recalculateOnGuaranteeChange = () => {
        if (daily > 0 && rateType === 1) {
            calculateHourly();
        } else if(hourly > 0 && rateType === 0) {
            calculateDaily();
        }
    }

    const recalculateOnHourlyChange = () => {
        if(guarantee > 0 && rateType === 0) {
            calculateDaily();
        }
    }

    const hoursToStraightTime = (hours) => {
        if (hours <= 8) {
            return hours;
        } else if (hours > 8 && hours <= 12) {
            return 8 + ((hours - 8) * 1.5);
        } else {
            return 14 + ((hours - 12) * 2);
        }
    }

    const calculateHourly = () => {
        if(guarantee === 0 || daily === 0) {
            setHourly(0);
            setValue(`${props.name}_hourly_rate`, '');
        } else {
            setHourly(parseFloat(Number(daily / hoursToStraightTime(guarantee)).toFixed(4)));
            setValue(`${props.name}_hourly_rate`,
                parseFloat(Number(daily / hoursToStraightTime(guarantee)).toFixed(4)));
        }
    }

    const calculateDaily = () => {
        if(guarantee === 0 || hourly === 0) {
            setDaily(0);
            setValue(`${props.name}_day_rate`, '');
        } else {
            setDaily(Math.round(hourly * hoursToStraightTime(guarantee)));
            setValue(`${props.name}_day_rate`, Math.round(hourly * hoursToStraightTime(guarantee)));
        }
    }

    useEffect(() => {
        recalculateOnDailyChange();
    }, [daily]);

    useEffect(() => {
        recalculateOnGuaranteeChange();
    }, [guarantee]);

    useEffect(() => {
        recalculateOnHourlyChange();
    }, [hourly]);

    return (
        <Card className="mb-3">
        <Card.Body >
            <Row>
                <Col xs={4}>
                        <Form.Group>
                            <Form.Label>Day rate</Form.Label>
                            <Controller
                                name={`${props.name}_day_rate`}
                                control={control}
                                rules={{
                                    required: {
                                        value: true,
                                        message: "Day rate is required"
                                    },
                                    validate: value => value > 0 || "Daily rate should be greater than 0"
                                }}
                                render={({   field,
                                             fieldState: { invalid}}) =>
                                <Form.Control
                                    aria-label={`${props.name}_day_rate`}
                                    {...field}
                                    type="number"
                                    placeholder="$"
                                    isInvalid={invalid}
                                    onChange={(event) => {
                                        if(event.target.value === '') {
                                            field.onChange(event.target.value);
                                        } else {
                                            field.onChange(parseFloat(Number(event.target.value)
                                                .toFixed(2)));
                                        }
                                        handleDailyChange(event);
                                    }}
                                    readOnly={rateType === 0}
                                    plaintext={rateType === 0}
                                    onClick={handleDailyClick}
                                />
                            }
                            />
                            <ErrorMessage
                                errors={formState.errors}
                                name={`${props.name}_day_rate`}
                                render = {
                                    ({ message }) =>
                                        <Form.Text className="text-danger">{message}</Form.Text>
                                }
                            />
                        </Form.Group>
                    {/*</Row>*/}
                </Col>

                <Col xs={4}>
                    <Form.Group>
                        <Form.Label>Guarantee</Form.Label>
                        <Controller
                            name={`${props.name}_guarantee`}
                            control={control}
                            rules={{
                                required: {
                                    value: true,
                                    message: "Guarantee is required"
                                },
                                validate: value => value > 0 || "Guarantee should be greater than 0"
                            }}
                            render={({  field,
                                        fieldState: { invalid }})=>
                                <Form.Control
                                    aria-label={`${props.name}_guarantee`}
                                    {...field}
                                    type="number"
                                    placeholder="hrs"
                                    isInvalid={invalid}
                                    onChange={(event) => {
                                        if(event.target.value === '') {
                                            field.onChange(event.target.value);
                                        } else {
                                            field.onChange(Number(event.target.value));
                                        }
                                        handleGuaranteeChange(event);
                                    }}
                                />
                            }
                        />
                        <ErrorMessage
                            errors={formState.errors}
                            name={`${props.name}_guarantee`}
                            render = {
                                ({ message }) =>
                                    <Form.Text className="text-danger">{message}</Form.Text>
                            }
                        />
                    </Form.Group>
                </Col>

                <Col xs={4}>
                    <Form.Group>
                        <Form.Label>Hourly rate</Form.Label>
                        <Controller
                            name={`${props.name}_hourly_rate`}
                            control={control}
                            rules={{
                                required: {
                                    value: true,
                                    message: "Hourly rate is required"
                                },
                                validate: value => value > 0 || "Hourly rate should be greater than 0"
                            }}
                            render={({  field,
                                        fieldState: { invalid }}) =>
                                <Form.Control
                                    aria-label={`${props.name}_hourly_rate`}
                                    {...field}
                                    type="number"
                                    placeholder="$"
                                    isInvalid={invalid}
                                    onChange={(event) => {
                                        if(event.target.value === '') {
                                            field.onChange(event.target.value);
                                        } else {
                                            field.onChange(parseFloat(Number(event.target.value).toFixed(4)));
                                        }
                                        handleHourlyChange(event);
                                    }}
                                    readOnly={rateType === 1}
                                    plaintext={rateType === 1}
                                    onClick={handleHourlyClick}
                                />
                            }
                        />
                        <ErrorMessage
                            errors={formState.errors}
                            name={`${props.name}_hourly_rate`}
                            render = {
                                ({ message }) =>
                                    <Form.Text className="text-danger">{message}</Form.Text>
                            }
                        />
                    </Form.Group>
                </Col>
            </Row>
        </Card.Body>
        </Card>
    )
}

export default RateWidget;