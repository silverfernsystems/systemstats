#! /usr/bin/env python
import sqlite3


def db():
	print('db')
	conn = sqlite3.connect('db.sqlite')
	cur = conn.cursor()

	# Check if table exists.
	# http://stackoverflow.com/questions/1601151/how-do-i-check-in-sqlite-whether-a-table-exists
	exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='cpu';"
	cur.execute(exists)
	if cur.fetchone() is None:
		create_cpu_table = "CREATE TABLE cpu ();"
	else:
		print("'cpu' table exists")
	# Insert new row into existing table
	# http://stackoverflow.com/questions/4253804/insert-new-column-into-table-in-sqlite

	conn.close()

def main():
	db()


if __name__ == '__main__':
	main()