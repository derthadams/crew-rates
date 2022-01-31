import React from 'react'
import AsyncCreatableSelect from "react-select/async-creatable";
import AsyncSelect from "react-select/async";
import axios from 'axios'
import customStyles from "./CustomSelectStyles";

const MINIMUM_QUERY_LENGTH = 3

class AsyncAPISelect extends React.Component {
    constructor(props) {
        super(props);
    };

    getParams = (sessionTokenExists, inputValue) => {
        let params = {};
        sessionTokenExists ?
            params = {
                q: inputValue,
                sessiontoken: this.props.getSessionToken()
            } :
            params = {
                q: inputValue
            };
        return params;
    };

    asyncOptions = (inputValue) =>
        inputValue.length >= MINIMUM_QUERY_LENGTH &&
        axios.get(this.props.url, {
            params: this.getParams(this.props.getSessionToken, inputValue)
        }).then(this.props.callback)

    noOptions = ({inputValue}) =>
        !inputValue ? `Search for ${this.props.search_text}...` :
        "No results found";

    render () {
        return (
            this.props.creatable ?
                <AsyncCreatableSelect
                    isClearable
                    aria-labelledby={this.props.ariaLabelledby}
                    defaultValue={this.props.lsmValue}
                    loadOptions={this.asyncOptions}
                    styles={customStyles(this.props.invalid)}
                    placeholder={''}
                    noOptionsMessage={this.noOptions}
                    isMulti={this.props.isMulti}
                    onChange={this.props.onChange}
                />
                :
                <AsyncSelect
                    isClearable
                    aria-labelledby={this.props.ariaLabelledby}
                    defaultValue={this.props.lsmValue}
                    loadOptions={this.asyncOptions}
                    styles={customStyles(this.props.invalid)}
                    placeholder={''}
                    noOptionsMessage={this.noOptions}
                    isMulti={this.props.isMulti}
                    onChange={this.props.onChange}
                />
        )
    }
}

export default AsyncAPISelect;