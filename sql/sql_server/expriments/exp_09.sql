alter table class add c_total int not null default 0;

create trigger t_inst_stu 
	on student
	for insert
	as
	if(@@rowcount>0)
	begin 
		declare @clsno char(6);
		select @clsno=clsNo from inserted;
		if @clsno is not null
			update class set c_total=c_total+1 where clsNo in (select clsNo from inserted);
	end;

create trigger t_dele_stu 
	on student
	for delete
	as
	if(@@rowcount>0)
	begin 
		declare @clsno char(6);
		select @clsno=clsNo from deleted;
		if @clsno is not null
			update class set c_total=c_total-1 where clsNo in (select clsNo from deleted);
	end;

create trigger t_update_stu 
	on student
	for update
	as
	if(@@rowcount>0)
	begin 
		declare @clsnoold char(6);
		declare @clsnonew char(6);
		select @clsnoold=clsNo from deleted;
		select @clsnonew=clsNo from inserted;
		if update(clsNo)
			update class set c_total=c_total-1 where clsNo in (select clsNo from deleted);
			update class set c_total=c_total+1 where clsNo in (select clsNo from inserted);
	end;

INSERT INTO student(sno,sname,ssex,clsNo,saddr,sage,height)
		  VALUES('20090119','李白','男','CS01','下关47#',20,1.76);
select * from class;

delete student where sno='20090119';
select * from class;

INSERT INTO student(sno,sname,ssex,clsNo,saddr,sage,height)
		  VALUES('20090119','李白','男','CS01','下关47#',20,1.76);
update student set clsNo='CS03' where sno='20090119';
select * from class;