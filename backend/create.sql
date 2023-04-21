CREATE DATABASE IF NOT EXISTS AniSong;

USE AniSong;

CREATE USER 'admin' @'%' IDENTIFIED BY 'password';

CREATE USER 'newuser' @'%' IDENTIFIED BY 'password2';

GRANT CREATE,
ALTER,
DROP,
INSERT
,
UPDATE
,
    DELETE,
SELECT
    on *.* TO 'admin' @'%' WITH GRANT OPTION;

GRANT CREATE,
ALTER,
DROP,
INSERT
,
UPDATE
,
    DELETE,
SELECT
    on AniSong.* TO 'newuser' @'%';

FLUSH PRIVILEGES;

CREATE TABLE Account(
    id BIGINT NOT NULL AUTO_INCREMENT,
    username VARCHAR(250) NOT NULL,
    email VARCHAR(250) NOT NULL,
    password VARCHAR(250) NOT NULL,
    profilPicture BLOB,
    isManager BOOLEAN NOT NULL,
    creationDate DATE,
    PRIMARY KEY(id),
    UNIQUE(username),
    UNIQUE(email)
);

CREATE TABLE Anime(
    id BIGINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(250) NOT NULL,
    posterImg BLOB NOT NULL,
    description TEXT NOT NULL,
    PRIMARY KEY(id),
    UNIQUE(name)
);

CREATE TABLE Type(
    id BIGINT NOT NULL AUTO_INCREMENT,
    typeName VARCHAR(250) NOT NULL,
    PRIMARY KEY(id),
    UNIQUE(typeName)
);

CREATE TABLE Author(
    id BIGINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(250) NOT NULL,
    posterImg BLOB NOT NULL,
    PRIMARY KEY(id),
    UNIQUE(name)
);

CREATE TABLE Music(
    id BIGINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(250) NOT NULL,
    posterImg BLOB,
    releaseDate DATE NOT NULL,
    id_Anime BIGINT NOT NULL,
    id_Type BIGINT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(id_Anime) REFERENCES Anime(id),
    FOREIGN KEY(id_Type) REFERENCES Type(id)
);

CREATE TABLE Review(
    id BIGINT NOT NULL AUTO_INCREMENT,
    noteVisual INT NOT NULL,
    noteMusic INT NOT NULL,
    description TEXT,
    creationDate DATE NOT NULL,
    id_Music BIGINT NOT NULL,
    id_Account BIGINT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(id_Music) REFERENCES Music(id),
    FOREIGN KEY(id_Account) REFERENCES Account(id)
);

CREATE TABLE Chante(
    id_Music BIGINT,
    id_Author BIGINT,
    PRIMARY KEY(id_Music, id_Author),
    FOREIGN KEY(id_Music) REFERENCES Music(id),
    FOREIGN KEY(id_Author) REFERENCES Author(id)
);

INSERT INTO
    Type (typeName)
VALUES
    ("Ost"),
    ("Ending"),
    ("Opening");