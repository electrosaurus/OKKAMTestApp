CREATE TABLE audience (
    id INTEGER,
    date DATE,
    respondent_id INTEGER,
    respondent_sex SMALLINT,
    respondent_age SMALLINT,
    weight DOUBLE PRECISION CHECK (weight >= 0),
    PRIMARY KEY (date, respondent_id)
);

COPY audience(id, date, respondent_id, respondent_sex, respondent_age, weight)
FROM '/etc/OKKAM_Middle Python Developer_data.csv'
DELIMITER ';'
CSV HEADER;
