#! /usr/bin/env python
import psutil
import json
from datetime import datetime


def system_stats():
	data = {}

	data['cpus'] = []
	for cpu_time in psutil.cpu_times(percpu=True):
		data['cpus'].append({'user': cpu_time.user, 'nice': cpu_time.nice,
			'idle': cpu_time.idle, 'iowait': cpu_time.iowait, 'irq': cpu_time.irq,
			'softirq': cpu_time.softirq, 'steal': cpu_time.steal, 'guest': cpu_time.guest,
			'guest_nice': cpu_time.guest_nice })

	for index, percent in enumerate(psutil.cpu_percent(interval=None, percpu=True)):
		data['cpus'][index]['percent'] = percent

	virtual_mem = psutil.virtual_memory()
	data['virtual_memory'] = {'total': virtual_mem.total,
	'available': virtual_mem.available,
	'percent': virtual_mem.percent,
	'used': virtual_mem.used,
	'free': virtual_mem.free,
	'active': virtual_mem.active,
	'inactive': virtual_mem.inactive,
	'buffers': virtual_mem.buffers,
	'cached': virtual_mem.cached}

	swap_mem = psutil.swap_memory()
	data['swap_memory'] = {'total': swap_mem.total,
	'used': swap_mem.total,
	'free': swap_mem.free,
	'percent': swap_mem.percent,
	'sin': swap_mem.sin,
	'sout': swap_mem.sout}

	# disk_partitions = psutil.disk_partitions()
	# print(disk_partitions)
	# for partition in psutil.disk_partitions():
	# 	usage = psutil.disk_usage(partition.mountpoint)
	# print(psutil.disk_io_counters(perdisk=True))
	
	processes = []
	for proc in psutil.process_iter():
		try:
			pinfo = proc.as_dict(attrs=['pid', 'name', 'memory_percent', 'cpu_percent', 'create_time'])
		except psutil.NoSuchProcess:
			pass
		else:
			processes.append(pinfo)

	data['processes'] = processes
	data['timestamp'] = datetime.now()
	return data


def main():
	print system_stats() #(json.dumps(system_stats()))


if __name__ == '__main__':
	main()