CREATE TEMPORARY TABLE network_name(
    name VARCHAR(128)
);

COPY network_name(name)
    FROM '/Users/derth/Documents/Business/Crewrates/data_csv/networks.csv'
    WITH(FORMAT csv, HEADER false);

INSERT INTO rates_network (name, uuid)
SELECT network_name.name, uuid_generate_v4() as uuid
FROM network_name
WHERE network_name.name not in
      (SELECT name FROM rates_network);