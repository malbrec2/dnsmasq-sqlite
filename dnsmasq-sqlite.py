#!/usr/bin/env python3

import os
import sys
import sqlite3

#TODO: add config file (/etc/dnsmasq-sqlite.conf ?)
#      read config file for db location


#TODO: add command line switches to control options
#      db location, config file

conn = sqlite3.connect('/var/lib/dnsmasq/dhcp_leases.db')

conn.execute("""CREATE TABLE IF NOT EXISTS leases(
                ipaddr text PRIMARY KEY,
                mac text NOT NULL,
                expire text NOT NULL,
                hostname text
            );""")

cmd = sys.argv[1]
mac = sys.argv[2]
ipaddr = sys.argv[3]

expire = os.environ["DNSMASQ_LEASE_EXPIRES"]

try:
    hostname = sys.argv[4]
except IndexError:
    hostname = ""

if(cmd == "add"):
    print('INSERT INTO leases VALUES ({},{},{},{})'.format(ipaddr, mac, expire, hostname))
    conn.execute('INSERT INTO leases VALUES (?,?,?,?)', (ipaddr, mac, expire, hostname))
elif(cmd == "old"):
    conn.execute("UPDATE leases SET mac = ?, expire = ?, hostname = ? WHERE ipaddr = ?", (mac, expire, hostname, ipaddr))
elif(cmd == "del"):
    print('DELETE FROM leases WHERE ipaddr = {}'.format(ipaddr))
    conn.execute('DELETE FROM leases WHERE ipaddr = ?', (ipaddr,))

conn.commit();
conn.close();
