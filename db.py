#! /usr/bin/env python
import sqlite3
from stats import system_stats


# Check if table exists.
# http://stackoverflow.com/questions/1601151/how-do-i-check-in-sqlite-whether-a-table-exists
def exists(cur, tablename):
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name='%s';" % tablename
    cur.execute(query)
    if cur.fetchone() is None:
        return False
    return True


def create_tables(conn, cur):
    # cpu
    if exists(cur, 'cpu') is False:
        print("Creating 'cpu' table...")
        create_cpu_table = """CREATE TABLE cpu (cpu_index INTEGER,
            softirq REAL, idle REAL, user REAL, guest_nice REAL,
            irq REAL, iowait REAL, percent REAL, steal REAL,
            guest REAL, nice REAL, time TIMESTAMP);"""
        cur.execute(create_cpu_table)
    else:
        print("Table 'cpu' exists.")

    # virtual memory
    if exists(cur, 'virtual_memory') is False:
        print("Creating 'virtual_memory' table...")
        create_virtual_memory_table = """CREATE TABLE virtual_memory (available INTEGER,
            cached INTEGER, used INTEGER, buffers INTEGER, inactive INTEGER, active INTEGER,
            total INTEGER, percent REAL, free INTEGER, time TIMESTAMP);"""
        cur.execute(create_virtual_memory_table)
    else:
        print("Table 'virtual_memory' exists.")

    # swap memory
    if exists(cur, 'swap_memory') is False:
        print("Creating 'swap_memory' table...")
        create_swap_memory_table = """CREATE TABLE swap_memory (used INTEGER, percent REAL,
            free INTEGER, sout INTEGER, total INTEGER, sin INTEGER, time TIMESTAMP);"""
        cur.execute(create_swap_memory_table)
    else:
        print("Table 'swap_memory' exists.")

    # processes
    if exists(cur, 'process') is False:
        print("Creating 'process' table...")
        create_process_table = """CREATE TABLE process (id INTEGER PRIMARY KEY, process_id INTEGER, name TEXT, started TIMESTAMP,
            UNIQUE (process_id, name, started));"""
        cur.execute(create_process_table)
    else:
        print("Table 'process' exists.")

    if exists(cur, 'process_snapshot') is False:
        print("Creating 'process_snapshot' table...")
        create_process_snapshot_table = """CREATE TABLE process_snapshot(process_id INTEGER,
            memory_percent REAL, cpu_percent REAL, time TIMESTAMP, FOREIGN KEY(process_id) REFERENCES process(id));"""
        cur.execute(create_process_snapshot_table)
    else:
        print("Table 'process_snapshot' exists.")

    # network
    if exists(cur, 'network') is False:
        print("Creating 'network' table...")
        create_network_table = """CREATE TABLE network (id INTEGER PRIMARY KEY, name TEXT, UNIQUE (name));"""
        cur.execute(create_network_table)
    else:
        print("Table 'network' exists.")

    if exists(cur, 'network_snapshot') is False:
        print("Creating 'network_snapshot' table...")
        create_network_snapshot_table = """CREATE TABLE network_snapshot(network_id INTEGER,
            bytes_sent INTEGER, bytes_recv INTEGER, packets_sent INTEGER, packets_recv INTEGER, errin INTEGER,
            errout INTEGER, dropin INTEGER, dropout INTEGER, time TIMESTAMP, FOREIGN KEY(network_id) REFERENCES network(id));"""
        cur.execute(create_network_snapshot_table)
    else:
        print("Table 'network_snapshot' exists.")

    # disk
    if exists(cur, 'disk') is False:
        print("Creating 'disk' table...")
        create_disk_table = """CREATE TABLE disk (id INTEGER PRIMARY KEY, name TEXT, UNIQUE (name));"""
        cur.execute(create_disk_table)
    else:
        print("Table 'disk' exists.")

    if exists(cur, 'disk_snapshot') is False:
        print("Creating 'disk_snapshot' table...")
        create_network_snapshot_table = """CREATE TABLE disk_snapshot(disk_id INTEGER,
            write_bytes INTEGER, read_count INTEGER, write_count INTEGER,
            read_time INTEGER, read_bytes INTEGER, write_time INTEGER, time TIMESTAMP, FOREIGN KEY(disk_id) REFERENCES disk(id));"""
        cur.execute(create_network_snapshot_table)
    else:
        print("Table 'disk_snapshot' exists.")


def db():
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()

    create_tables(conn, cur)

    stats = system_stats()
    timestamp = stats['timestamp']

    # cpu
    cpu_snapshots = []
    for index, cpu in enumerate(stats['cpus']):
        cpu_snapshots.append((index, cpu['softirq'], cpu['idle'], cpu['user'], cpu['guest_nice'], cpu['irq'],
            cpu['iowait'], cpu['percent'], cpu['steal'], cpu['guest'], cpu['nice'], timestamp))
    cur.executemany('INSERT INTO cpu VALUES (?,?,?,?,?,?,?,?,?,?,?,?);', cpu_snapshots)
    conn.commit()

    # virtual memory
    vm = stats['virtual_memory']
    virtual_memory_snapshot = (vm['total'], vm['available'], vm['percent'], vm['used'], vm['free'],
        vm['active'], vm['inactive'], vm['buffers'], vm['cached'], timestamp)
    cur.execute('INSERT INTO virtual_memory VALUES (?,?,?,?,?,?,?,?,?,?)', virtual_memory_snapshot)
    conn.commit()

    # swap memory
    sm = stats['swap_memory']
    swap_memory_snapshot = (sm['total'], sm['used'], sm['free'], sm['percent'], sm['sin'], sm['sout'], timestamp)
    cur.execute('INSERT INTO swap_memory VALUES (?,?,?,?,?,?,?)', swap_memory_snapshot)
    conn.commit()

    # network
    networks = []
    for index, network in enumerate(stats['network']):
        networks.append((index, network))
    try:
        cur.executemany('INSERT INTO network VALUES (?, ?);', networks)
    except:
        pass
    conn.commit()

    # disk
    disks = []
    for index, disk in enumerate(stats['disk']):
        disks.append((index, disk))
    try:
        cur.executemany('INSERT INTO disk VALUES (?, ?);', disks)
    except:
        pass
    conn.commit()

    # Print stats
    cur.execute('SELECT COUNT(*) FROM cpu;')
    print('CPU snapshots: %d records.' % cur.fetchone()[0])
    for row in cur.execute('SELECT * FROM cpu ORDER BY cpu_index, time;'):
        print row

    cur.execute('SELECT COUNT(*) FROM virtual_memory;')
    print('Virtual Memory: %d records.' % cur.fetchone()[0])
    for row in cur.execute('SELECT * FROM virtual_memory ORDER BY time;'):
        print row

    cur.execute('SELECT COUNT(*) FROM swap_memory;')
    print('Swap Memory: %d records.' % cur.fetchone()[0])
    for row in cur.execute('SELECT * FROM swap_memory ORDER BY time;'):
        print row
    
    cur.execute('SELECT COUNT(*) FROM network;')
    print('Networks: %d records.' % cur.fetchone()[0])
    for row in cur.execute('SELECT * FROM network ORDER BY id;'):
        print row

    cur.execute('SELECT COUNT(*) FROM disk;')
    print('Disks: %d records.' % cur.fetchone()[0])
    for row in cur.execute('SELECT * FROM disk ORDER BY id;'):
        print row

    conn.close()

def main():
    db()


if __name__ == '__main__':
    main()
