-- migrate:up

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS film(
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name VARCHAR(80) NOT NULL CHECK(LENGTH(name) > 0),
	description VARCHAR(1024) NOT NULL CHECK(LENGTH(description) > 0),
	rating decimal NOT NULL CHECK(rating >= 0)
);

CREATE TABLE IF NOT EXISTS actor(
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name VARCHAR(128) NOT NULL CHECK(LENGTH(name) > 0),
	surname VARCHAR(128) NOT NULL CHECK(LENGTH(surname) > 0),
	age INTEGER NOT NULL CHECK(age >= 0)
);

CREATE TABLE IF NOT EXISTS film_to_actor (
	film_id uuid REFERENCES film(id),
	actor_id uuid REFERENCES actor(id),
	PRIMARY KEY(film_id, actor_id)
);

-- migrate:down