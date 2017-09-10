create procedure p_stu_infol
as
begin
	select * from student where sage<21;
end;

create procedure p_stu_indo2
	@sno char(8)
as 
begin
	select * from student where sage =(select sage from student where sno=@sno);
end;

create procedure p_stu_info3
	@sno char(8)
as 
begin
	select * from student where sno=@sno;
end;

create procedure p_stu_grade
	@sno char(8)
as 
begin
	select * from sc where sno=@sno;
end;

exec p_stu_infol;
exec p_stu_indo2'20090101';
exec p_stu_info3'20090101';
exec p_stu_grade'20090101';