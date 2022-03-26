import React , { useState, useEffect } from 'react';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import Card from "react-bootstrap/Card";
import { useFormContext, Controller } from "react-hook-form"
import {ErrorMessage} from "@hookform/error-message";


function RateWidget({name}) {
    const { control, setValue, getValues , formState, trigger } = useFormContext();
    const [daily, setDaily] = useState(getValues(`${name}_day_rate`) || 0);
    const [guarantee, setGuarantee] = useState(getValues(`${name}_guarantee`) || 0);
    const [hourly, setHourly] = useState(getValues(`${name}_hourly_rate`) || 0);
    const [rateType, setRateType] = useState(1);

    const getHourly = () => getValues(`${name}_hourly_rate`) === '' ?
            0 : Number(getValues(`${name}_hourly_rate`));
    const getDaily = () => getValues(`${name}_day_rate`) === '' ?
            0 : Number(getValues(`${name}_day_rate`));
    const getGuarantee = () => getValues(`${name}_guarantee`) === '' ?
            0 : Number(getValues(`${name}_guarantee`));

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
        if((getGuarantee() === 0 && getDaily() > 0) || getDaily() === 0) {
            setValue(`${name}_day_rate`, '');
        }
    }

    const handleDailyClick = (event) => {
        setRateType(1);
        if((getGuarantee() === 0 && getHourly() > 0) || getHourly() === 0) {
            setValue(`${name}_hourly_rate`, '');
        }
    }

    const recalculateOnDailyChange = () => {
        if (getGuarantee() > 0 && rateType === 1) {
            calculateHourly();
        }
    }

    const recalculateOnGuaranteeChange = () => {
        if (getDaily() > 0 && rateType === 1) {
            calculateHourly();
        } else if(getHourly() > 0 && rateType === 0) {
            calculateDaily();
        }
    }

    const recalculateOnHourlyChange = () => {
        if(getGuarantee() > 0 && rateType === 0) {
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
        if(getGuarantee() === 0 || getDaily() === 0) {
            setValue(`${name}_hourly_rate`, '');
        } else {
            setHourly(parseFloat(Number(getDaily() / hoursToStraightTime(getGuarantee())).toFixed(4)));
            setValue(`${name}_hourly_rate`,
                    parseFloat(Number(getDaily() / hoursToStraightTime(getGuarantee())).toFixed(4)));
        }
    }

    const calculateDaily = () => {
        if(getGuarantee() === 0 || getHourly() === 0) {
            setValue(`${name}_day_rate`, '');
        } else {
            setDaily(Math.round(getHourly() * hoursToStraightTime(getGuarantee())));
            setValue(`${name}_day_rate`, Math.round(getHourly() * hoursToStraightTime(getGuarantee())));
        }
    }

    useEffect (async () => {
        recalculateOnDailyChange();
        if(formState.errors[`${name}_day_rate`]) {
            await trigger(`${name}_day_rate`)
        }
    }, [daily]);

    useEffect(async () => {
        recalculateOnGuaranteeChange();
        if(formState.errors[`${name}_guarantee`]) {
            await trigger(`${name}_guarantee`)
        }
    }, [guarantee]);

    useEffect(async () => {
        recalculateOnHourlyChange();
        if(formState.errors[`${name}_hourly_rate`]) {
            await trigger(`${name}_hourly_rate`)
        }
    }, [hourly]);

    return (
        <Card className="mb-3">
        <Card.Body >
            <Row>
                <Col xs={4}>
                        <Form.Group>
                            <Form.Label>Day rate</Form.Label>
                            <Controller
                                name={`${name}_day_rate`}
                                control={control}
                                rules={{
                                    required: {
                                        value: true,
                                        message: "Day rate is required"
                                    },
                                    validate: value => value > 0 || "Day rate should be greater than 0"
                                }}
                                render={({   field,
                                             fieldState: { invalid}}) =>
                                <Form.Control
                                    aria-label={`${name}_day_rate`}
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
                                name={`${name}_day_rate`}
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
                            name={`${name}_guarantee`}
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
                                    aria-label={`${name}_guarantee`}
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
                            name={`${name}_guarantee`}
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
                            name={`${name}_hourly_rate`}
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
                                    aria-label={`${name}_hourly_rate`}
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
                            name={`${name}_hourly_rate`}
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