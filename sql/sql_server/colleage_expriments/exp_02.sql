create table class
	(clsNo CHAR(6) PRIMARY KEY,
	clsName VARCHAR(16) NOT NULL,
	Director VARCHAR(6),
	Speciality VARCHAR(30));
create table student 
	(sno CHAR(8) PRIMARY KEY,
	sname VARCHAR(10) NOT NULL,
	ssex CHAR(2) CHECK(ssex IN('ÄÐ','Å®')),
	clsNo CHAR(6),
	saddr VARCHAR(20),
	sage FLOAT(3) CHECK(sage BETWEEN 10 AND 30),
	height NUMERIC(4,2),
	FOREIGN KEY (clsNo) REFERENCES class(clsNo)); 
create table course
	(cno CHAR(4) PRIMARY KEY,
	cname VARCHAR(16) NOT NULL,
	cpno CHAR(4),
	Ccredit NUMERIC(2,1),
	FOREIGN KEY (cpno) REFERENCES course(cno));
create table sc
	(sno CHAR(8),
	cno CHAR(4),
	grade NUMERIC(3,1));
create table student1 
	(sno CHAR(8) PRIMARY KEY,
	sname VARCHAR(10) NOT NULL,
	ssex CHAR(2) CHECK(ssex IN('ÄÐ','Å®')),
	clsNo CHAR(6),
	saddr VARCHAR(20),
	sage FLOAT(3) CONSTRAINT C1 CHECK(sage BETWEEN 10 AND 30),
	height NUMERIC(4,2),
	FOREIGN KEY (clsNo) REFERENCES class(clsNo)); 
ALTER TABLE student1 ADD S_entrance DATETIME;
ALTER TABLE student1 DROP CONSTRAINT C1;
ALTER TABLE student1 ADD CHECK(sage BETWEEN 10 AND 40);
ALTER TABLE student1 ALTER COLUMN saddr VARCHAR(40);
drop table student1;
	