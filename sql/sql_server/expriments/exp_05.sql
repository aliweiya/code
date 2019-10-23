create index Stusname on student(sname DESC) ;
create unique index Coucname on course(cname);
create index SCno on sc(sno ASC,Cno ASC,grade DESC);

drop index Stusname on student;
