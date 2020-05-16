CREATE TABLE users
(
    user_id bigint NOT NULL,
    balance numeric(10, 2) NOT NULL,
    work timestamp without time zone,
    PRIMARY KEY (user_id)
);