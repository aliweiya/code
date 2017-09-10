create login cxp with password='123',default_database=EDUC;

create user p for login cxp with default_schema=dbo;

create role 崔平
grant update(sno),select on student to 崔平；

drop role 崔平;

exec sp_adduser 'cxp','p','崔平'