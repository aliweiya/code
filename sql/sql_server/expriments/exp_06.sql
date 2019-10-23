update student set sname='张三' where sname='李杰';
select * from student;
select student.sno,student.sname from student,class where student.clsNo=class.clsNo and class.Speciality='计算机应用';
select distinct sno from sc;
select sno,0.75*grade from sc where grade>80 and grade <90 and cno='0001';
select student.* from student,class where student.clsNo=class.clsNo and (class.Speciality='计算机应用' or class.Speciality like '数学') and sname like '张%';
select sno,grade from sc where grade>(select sc.grade from sc,student where student.sno=sc.sno and student.sname='张三' and sc.cno='0001');
select sname from student where not exists(select * from sc where cno='0002' and sno=student.sno);