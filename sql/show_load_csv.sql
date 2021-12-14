CREATE TEMPORARY TABLE show_title(
    title VARCHAR(128)
);

COPY show_title(title)
    FROM '/Users/derth/Documents/Business/Crewrates/data_csv/shows.csv'
    WITH(FORMAT csv, HEADER false);

INSERT INTO rates_show (title, uuid)
SELECT show_title.title, uuid_generate_v4() as uuid
FROM show_title
WHERE show_title.title not in
      (SELECT title FROM rates_show);