CREATE DATABASE blog;
use blog;

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  username varchar(1024) CHARACTER SET ascii UNIQUE NOT NULL,
  password varchar(1024) NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title varchar(1024) NOT NULL,
  body varchar(1024) NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE rireki (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  dir_path varchar(1024) NOT NULL,
  tex varchar(1024) NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

INSERT INTO user (username, password)
VALUES ('oda', 'oda');

INSERT INTO rireki (dir_path, tex, author_id)
VALUES ('/app/files/0/', 'platex', 1);
