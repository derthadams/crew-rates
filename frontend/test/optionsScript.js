const optionsScript = "<div>  <script id=\"genreOptions\" type=\"application/json\">" +
        "[{\"value\": \"RE\", \"label\": \"Reality\"}, " +
        "{\"value\": \"DO\", \"label\": \"Documentary\"}, " +
        "{\"value\": \"GA\", \"label\": \"Game Show\"}, " +
        "{\"value\": \"LI\", \"label\": \"Live Show\"}, " +
        "{\"value\": \"TA\", \"label\": \"Talk Show\"}, " +
        "{\"value\": \"JU\", \"label\": \"Judge Show\"}, " +
        "{\"value\": \"OT\", \"label\": \"Other Unscripted\"}, " +
        "{\"value\": \"SC\", \"label\": \"Scripted\"}]</script>\n" +
        "  <script id=\"unionOptions\" type=\"application/json\">" +
        "[{\"value\": \"NO\", \"label\": \"Non-Union\"}, " +
        "{\"value\": \"IA\", \"label\": \"IATSE\"}, " +
        "{\"value\": \"NA\", \"label\": \"NABET\"}]</script>\n" +
        "  <script id=\"apiUrls\" type=\"application/json\">" +
        "{\"autocomplete\": \"/api/autocomplete/\", " +
        "\"details\": \"/api/details/\", " +
        "\"shows\": \"/api/shows/\", " +
        "\"companies\": \"/api/companies/\", " +
        "\"networks\": \"/api/networks/\", " +
        "\"job-titles\": \"/api/job-titles/\", " +
        "\"add-rate-api\": \"/api/add-rate/\"}</script></div>";

export default optionsScript;