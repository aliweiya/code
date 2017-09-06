import sqlite3

SQL = """
	CREATE TABLE IF NOT EXISTS userinfo(
		username TEXT NOT NULL,
		password TEXT,
		PRIMARY KEY (username)
		);
"""

UPDATE = """
	UPDATE userinfo SET password='"123456"' WHERE username='MrTurtle';
"""

INSERT = """
	INSERT INTO userinfo VALUES('MrTurtle', '123');
"""

FIND = """
	SELECT * FROM userinfo;
"""

DELETE = """
	DELETE FROM userinfo WHERE username = 'MrTurtle';
"""

conn = sqlite3.connect('userinfo.db')

cur = conn.cursor()

cur.execute(SQL)
# cur.execute(DELETE)
cur.execute(INSERT)
conn.commit()
# cur.execute(FIND)
# cur.execute(UPDATE)