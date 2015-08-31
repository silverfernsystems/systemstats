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

	disk_io = psutil.disk_io_counters(perdisk=True)

	disk_data = {}
	for disk in disk_io:
		disk_data[disk] = {}
		disk_data[disk]['read_count'] = disk_io[disk].read_count
		disk_data[disk]['write_count'] = disk_io[disk].write_count
		disk_data[disk]['read_bytes'] = disk_io[disk].read_bytes
		disk_data[disk]['write_bytes'] = disk_io[disk].write_bytes
		disk_data[disk]['read_time'] = disk_io[disk].read_time
		disk_data[disk]['write_time'] = disk_io[disk].write_time

	data['disk'] = disk_data

	net_io = psutil.net_io_counters(pernic=True)
	net_data = {}
	for net in net_io:
		net_data[net] = {}
		net_data[net]['bytes_sent'] = net_io[net].bytes_sent
		net_data[net]['bytes_recv'] = net_io[net].bytes_recv
		net_data[net]['packets_sent'] = net_io[net].packets_sent
		net_data[net]['packets_recv'] = net_io[net].packets_recv
		net_data[net]['errin'] = net_io[net].errin
		net_data[net]['errout'] = net_io[net].errout
		net_data[net]['dropin'] = net_io[net].dropin
		net_data[net]['dropout'] = net_io[net].dropout
	
	data['network'] = net_data

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
	print system_stats()['network'] # 


if __name__ == '__main__':
	main()