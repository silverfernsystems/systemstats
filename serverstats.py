#! /usr/bin/env python

import daemon
import time
import argparse
from setproctitle import setproctitle
from server import Server


def web(port):
    server = Server(port)


def run(daemonize, port=8888):
    if daemonize:
        print("Daemonizing application on port %d." % port)
        with daemon.DaemonContext():
            web(port)
    else:
        print("Running application on port %d." % port)
        web(port)


def main():
    setproctitle("SystemStats")
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="the port to use. default is 8888.")
    parser.add_argument("-d", action="store_true", help="daemonize application.")
    args = parser.parse_args()

    daemonize = args.d
    port = args.port or 8888
    run(daemonize, int(port))


if __name__ == "__main__":
    main()

