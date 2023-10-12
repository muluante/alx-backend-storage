-- Creates a table users with attribures:
--       id, integer, never null, auto increment and primary key
--       email, string (255 characters), never null and unique
--       name, string (255 characters)
--       country, enumeration of countries: US, CO and TN, never null
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
	id INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255),
	country ENUM('US', 'CO', 'TN') NOT NULL,
	PRIMARY KEY (id)
	);
