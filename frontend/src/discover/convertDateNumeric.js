export default function convertDateNumeric(dateString) {
    const eight_hours = 28800000;
    const date = new Date(dateString);
    date.setTime(date.getTime() + eight_hours);

        return date.toLocaleDateString("en-US", {
            month: "numeric",
            day: "numeric",
            year: "numeric",
        });
}
