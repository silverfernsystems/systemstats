#! /usr/bin/env python
import ConfigParser


def load_config():
	config = ConfigParser.ConfigParser()
	config.readfp(open('defaults.cfg'))
	processes = config.get('Processes', 'names').split(',')
	print(processes)


def main():
	load_config()


if __name__ == '__main__':
	main()