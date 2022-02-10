export default function convertDate(dateString, format = "long") {
    const eight_hours = 28800000;
    const date = new Date(dateString);
    date.setTime(date.getTime() + eight_hours);
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
