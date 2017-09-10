INSERT INTO class(clsNo,clsName,Director,Speciality)
		  VALUES('CS01','计算机一班','张宁','计算机应用');
INSERT INTO class(clsNo,clsName,Director,Speciality)
		  VALUES('CS02','计算机二班','王宁','计算机应用');
INSERT INTO class(clsNo,clsName,Director,Speciality)
		  VALUES('MT04','数学四班','陈晨','数学');
INSERT INTO class(clsNo,clsName,Director,Speciality)
		  VALUES('PH08','物理八班','葛格','物理');
INSERT INTO class(clsNo,clsName,Director,Speciality)
		  VALUES('GL02','地理二班','张四','应用地理');
INSERT INTO class(clsNo,clsName,Director,Speciality)
		  VALUES('CS03','计算机三班','诸葛亮','计算机应用');
INSERT INTO class(clsNo,clsName,Director,Speciality)
		  VALUES('GL04','地理四班','曹操','应用地理');
INSERT INTO class(clsNo,clsName,Director,Speciality)
		  VALUES('MT05','数学五班','刘备','数学');
INSERT INTO class(clsNo,clsName,Director,Speciality)
		  VALUES('CS07','计算机七班','鸣人','计算机应用');
INSERT INTO class(clsNo,clsName,Director,Speciality)
		  VALUES('PH09','物理九班','鼬','物理');
select * from class;
INSERT INTO student(sno,sname,ssex,clsNo,saddr,sage,height)
		  VALUES('20090101','王军','男','CS01','下关40#',20,1.76);
INSERT INTO student(sno,sname,ssex,clsNo,saddr,sage,height)
		  VALUES('20090102','李杰','男','CS01','江边路96#',22,1.72);
INSERT INTO student(sno,sname,ssex,clsNo,saddr,sage,height)
		  VALUES('20090306','王彤','女','MT04','中央路94#',19,1.65);
INSERT INTO student(sno,sname,ssex,clsNo,saddr,sage,height)
		  VALUES('20090107','吴秒','女','PH08','莲化小区74#',18,1.60);
INSERT INTO student(sno,sname,ssex,clsNo,saddr,sage,height)
		  VALUES('20090108','诸葛亮','男','CS03','兴化路10#',21,1.83);
INSERT INTO student(sno,sname,ssex,clsNo,saddr,sage,height)
		  VALUES('20090305','鼬','男','PH09','木叶36#',22,1.80);
INSERT INTO student(sno,sname,ssex,clsNo,saddr,sage,height)
		  VALUES('20090110','曹操','男','GL04','魏国7#',22,1.73);
INSERT INTO student(sno,sname,ssex,clsNo,saddr,sage,height)
		  VALUES('20090113','刘备','男','MT05','蜀国4#',18,1.75);
INSERT INTO student(sno,sname,ssex,clsNo,saddr,sage,height)
		  VALUES('20090117','鸣人','男','CS07','木叶18#',17,1.78);
select * from student;

INSERT INTO course(cno,cname,cpno,Ccredit)
		  VALUES('0001','高等数学',null,6);
INSERT INTO course(cno,cname,cpno,Ccredit)
		  VALUES('0003','计算机基础','0001',3);
INSERT INTO course(cno,cname,cpno,Ccredit)
		  VALUES('0007','物理','0001',4);
INSERT INTO course(cno,cname,cpno,Ccredit)
		  VALUES('0005','英语',NULL,3);
INSERT INTO course(cno,cname,cpno,Ccredit)
		  VALUES('0006','数据结构',null,4);
INSERT INTO course(cno,cname,cpno,Ccredit)
		  VALUES('0002','离散数学',NULL,2);
select * from course;

INSERT INTO sc(sno,cno,grade)
		  VALUES('20090101','0001',90);
INSERT INTO sc(sno,cno,grade)
		  VALUES('20090101','0007',86);
INSERT INTO sc(sno,cno,grade)
		  VALUES('20090102','0001',87);
INSERT INTO sc(sno,cno,grade)
		  VALUES('20090101','0003',93);
INSERT INTO sc(sno,cno,grade)
		  VALUES('20090306','0001',87);
INSERT INTO sc(sno,cno,grade)
		  VALUES('20090306','0003',93);
INSERT INTO sc(sno,cno,grade)
		  VALUES('20090106','0007',85);
INSERT INTO sc(sno,cno,grade)
		  VALUES('20090306','0007',90);
INSERT INTO sc(sno,cno,grade)
		  VALUES('20090102','0003',96);
INSERT INTO sc(sno,cno,grade)
		  VALUES('20090306','0001',90);
select * from sc;

INSERT INTO student(sno,sname,ssex,clsNo,sage)
		  VALUES('20091101','张三','男','CS01',19);
select * from student;

update student set clsNo='CS02' where clsNo='CS01' and sage<20;
select * from student;

delete student where clsNo='CS02' and sage<20;
select * from student;