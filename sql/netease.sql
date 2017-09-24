CREATE DATABASE NetEaseMusic;

CREATE TABLE Singer(
    singerId VARCHAR(10),
    singerName VARCHAR(100)
);
    
CREATE TABLE Album(
    albumId VARCHAR(10),
    albumSingerId VARCHAR(10),
    FOREIGN KEY (albumSingerId) REFERENCES Singer(singerId)
);
    
-- a song is not necessarily in a album, or a singer, 
-- maybe just a user
CREATE TABLE Song(
    songID VARCHAR(20),
    songAlbumId VARCHAR(10), 
    songSingerId VARCHAR(10),
    commentCount INT,
    PRIMARY KEY (songID),
    FOREIGN KEY (songAlbumId) REFERENCES Album(albumId),
    FOREIGN KEY (songSingerId) REFERENCES Singer(singerId)
);
    
CREATE TABLE NetEaseUser(
    userid VARCHAR(10),
    username VARCHAR(10)
);

CREATE TABLE Comments(
    songId VARCHAR(10),
    content VARCHAR(10),
    username VARCHAR(10),
    commentTime DATETIME
);