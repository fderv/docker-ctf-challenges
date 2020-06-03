/*DROP DATABASE IF EXISTS user_db;*/
/*CREATE DATABASE user_db;*/
USE user_db;

DROP TABLE IF EXISTS users;
CREATE TABLE users  (
	id int(11) NOT NULL AUTO_INCREMENT,
	email varchar(64) NOT NULL,
	password varchar(255) NOT NULL,
	PRIMARY KEY(id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO users (id, email, password) VALUES (1, "admin@admin.x", "y3jCxs5TkfBdcH39SSHvm3JZ");
