function customStyles(invalid) {
    return ({
            control: (base, state) => (
                invalid ? {
                        ...base,
                        boxShadow: state.isFocused ? "0 0 0 .25rem #F2D0D2 !important" : base.boxShadow,
                        borderColor: "#dc3545 !important"
                    }:
                    {
                        ...base,
                        borderColor: state.isFocused ? '#88B9FC' : '#CED4DA',
                        "&:hover": {
                            borderColor: state.isFocused ? '#88B9FC' : '#CED4DA'
                        },
                        boxShadow: state.isFocused ? '0 0 0 .25rem rgba(13, 110, 253, .25)': base.boxShadow
                    }
            ),
            placeholder: (provided, state) => ({
                ...provided,
                color: '#6D757D',
                marginLeft: 4,
            })
        })
}

export default customStyles;