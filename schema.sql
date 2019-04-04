drop table if exists country;
create table country (
  id serial PRIMARY KEY,
  name text not null
);

drop table if exists author;
create table author (
  id serial PRIMARY KEY,
  country_id integer REFERENCES country (id),
  name text not null
);

drop table if exists book;
create table book (
  id serial PRIMARY KEY,
  author_id integer REFERENCES author (id),
  title text not null,
  isbn text
);
