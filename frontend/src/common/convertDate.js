export default function convertDate(dateString, format = "long") {
    const date = new Date(dateString);
    const timezoneOffsetMs = date.getTimezoneOffset() * 60000
    date.setTime(date.getTime() + timezoneOffsetMs)
    if(isNaN(date)) {
        return "";
    }
    if (format === "long") {
        return date.toLocaleDateString("en-US", {
            month: "long",
            day: "numeric",
            year: "numeric",
        });
    } else if (format === "numeric") {
        return date.toLocaleDateString("en-US", {
            month: "numeric",
            day: "numeric",
            year: "numeric",
        });
    }
}
