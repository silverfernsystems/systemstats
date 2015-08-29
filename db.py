#! /usr/bin/env python
import sqlite3
from stats import system_stats

def db():
	conn = sqlite3.connect('db.sqlite')
	cur = conn.cursor()

	# Check if table exists.
	# http://stackoverflow.com/questions/1601151/how-do-i-check-in-sqlite-whether-a-table-exists
	exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='cpu';"
	cur.execute(exists)
	if cur.fetchone() is None:
		print("creating 'cpu' table")
		create_cpu_table = """CREATE TABLE cpu (cpu_index integer,
			softirq REAL, idle REAL, user REAL, guest_nice REAL,
			irq REAL, iowait REAL, percent REAL, steal REAL,
			guest REAL, nice REAL, time TIMESTAMP);"""
		cur.execute(create_cpu_table)
	else:
		print("'cpu' table exists")

	exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='process';"
	cur.execute(exists)
	if cur.fetchone() is None:
		print("creating 'process' table")
		create_process_table = """CREATE TABLE process (id INTEGER PRIMARY KEY, process_id INTEGER, name TEXT, started TIMESTAMP,
			UNIQUE (process_id, name, started));"""
		cur.execute(create_process_table)
	else:
		print("'process' table exists")

	exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='process_snapshot';"
	cur.execute(exists)
	if cur.fetchone() is None:
		print("creating 'process_snapshot' table")
		create_process_snapshot_table = """CREATE TABLE process_snapshot(process_id INTEGER,
			memory_percent REAL, cpu_percent REAL, time TIMESTAMP, FOREIGN KEY(process_id) REFERENCES process(id));"""
		cur.execute(create_process_snapshot_table)
	else:
		print("'process_snapshot' table exists")



	stats = system_stats()
	timestamp = stats['timestamp']
	cpu_snapshots = []
	for index, cpu in enumerate(stats["cpus"]):
		cpu_snapshots.append((index, cpu['softirq'], cpu['idle'], cpu['user'], cpu['guest_nice'], cpu['irq'],
			cpu['iowait'], cpu['percent'], cpu['steal'], cpu['guest'], cpu['nice'], timestamp))
	cur.executemany('INSERT INTO cpu VALUES (?,?,?,?,?,?,?,?,?,?,?,?);', cpu_snapshots)
	conn.commit()

	for row in cur.execute('SELECT * FROM cpu ORDER BY cpu_index, time;'):
		print row

	cur.execute('SELECT COUNT(*) FROM cpu;')
	print("%d records in database." % cur.fetchone()[0])

	conn.close()

def main():
	db()


if __name__ == '__main__':
	main()