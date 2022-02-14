export default function convertDateNumeric(dateString) {
    const date = new Date(dateString);
    const timezoneOffsetMs = date.getTimezoneOffset() * 60000
    date.setTime(date.getTime() + timezoneOffsetMs)

        return date.toLocaleDateString("en-US", {
            month: "numeric",
            day: "numeric",
            year: "numeric",
        });
}
