-- heroku pg:psql < initial_data.sql

-- Countries
INSERT INTO country (id, name) VALUES (1, 'United States');
INSERT INTO country (id, name) VALUES (2, 'England');
INSERT INTO country (id, name) VALUES (3, 'Argentina');
INSERT INTO country (id, name) VALUES (4, 'Scotland');

-- Authors
INSERT INTO author (id, country_id, name) VALUES (1, 1, 'Edgar Allan Poe');
INSERT INTO author (id, country_id, name) VALUES (2, 1, 'Mark Twain');
INSERT INTO author (id, country_id, name) VALUES (3, 4, 'Arthur Conan Doyle');
INSERT INTO author (id, country_id, name) VALUES (4, 3, 'Jorge Luis Borges');
