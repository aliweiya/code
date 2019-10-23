create view V_SC_G(sno,sname,cno,cname,grade) as select student.sno,sname,sc.cno,cname,grade from student,course,sc where student.sno=sc.sno  and course.cno=sc.cno;
select * from V_SC_G;
create view V_YEAR(sno,sname,sbirth) as select sno,sname,year(getdate())-sage from student;
select * from V_YEAR;

create view V_AVG_S_G(sno,csum,gavg) as select sno,count(*),avg(grade) from sc group by sno;
select * from V_AVG_S_G;

create view V_AVG_C_G(cno,ssum,cavg) as select cno,count(*),avg(grade) from sc group by cno;
select * from V_AVG_C_G;

select sno,sname,grade from V_SC_G where sno in (select sno from V_AVG_S_G  where gavg>=90);

select sc.sno,sc.cno,sc.grade,V_AVG_C_G.cavg from sc,V_AVG_C_G where sc.cno=V_AVG_C_G.cno and sc.grade>V_AVG_C_G.cavg;

select sno,sname from V_YEAR where sbirth=1995;