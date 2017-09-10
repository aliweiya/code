select count(*) from student;
select count(distinct sno) from sc;
select cno,count(sno) from sc group by cno;
select sno,sname from student where sno in(select sno from sc group by sno having count(*)>2);
