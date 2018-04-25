# -*- coding: utf-8 -*-
import re
import time
from random import randint

def mac_string_2_array(mac):
    return [int(i, 16) for i in mac.split(':')]


def ip_string_2_array(mac):
    return [int(i) for i in mac.split('.')]

def netmask_to_cidr(netmask):
    return sum([bin(int(x)).count('1') for x in netmask.split('.')])

def uptime():
    with open('/proc/uptime', 'r') as f:
      return int(float(f.readline().split()[0]))

def get_if_table(data):
    # XXX FIXME
    if_list = [ 'eth0', 'eth1' ]
    if_table = []

    if_data = data['ifstat']

    for (iface,info) in if_data.items():
      if iface in if_list:
        if_entry = {
                 'drops': info["rx_dropped"] + info["tx_dropped"],
                 'enable': True,
                 'full_duplex': True,
                 'gateways': [
                     data['ip'][iface]['gateway'] if 'gateway' in data['ip'][iface] else ''
                 ],
                 'ip': data['ip'][iface]['address'],
                 'latency': randint(0, 30), # TODO FIXME
                 'mac': data['macs'][iface],
                 'name': iface,
                 'nameservers': data['nameservers'],
                 'netmask': data['ip'][iface]['netmask'],
                 'num_port': 1,
                 'rx_bytes': info["rx_bytes"],
                 'rx_dropped': info["rx_dropped"],
                 'rx_errors': info["rx_errors"],
                 'rx_multicast': info["rx_multicast"],
                 'rx_packets': info["rx_packets"],
                 'speed': 1000,
                 'speedtest_lastrun': int(time.time()),
                 'speedtest_ping': randint(0, 2000),
                 'speedtest_status': 'Idle',
                 'tx_bytes': info["tx_bytes"],
                 'tx_dropped': info["tx_dropped"],
                 'tx_errors': info["tx_errors"],
                 'tx_packets': info["tx_packets"],
                 'up': True,
                 'uptime': uptime(),
                 'xput_down': randint(0, 100), # TODO FIXME
                 'xput_up': randint(0, 30) # TODO FIXME
             }
        if_table.append(if_entry)
    return if_table

def get_network_table(data):
    # XXX FIXME
    if_list = [ 'eth0', 'eth1' ]
    lan_if = 'eth1'
    network_table = []

    for iface in if_list:
      net_entry = {
                 'address': '%s/%s' % (data['ip'][iface]['address'], netmask_to_cidr(data['ip'][iface]['netmask'])),
                 'addresses': [
                     '%s/%s' % (data['ip'][iface]['address'], netmask_to_cidr(data['ip'][iface]['netmask']))
                 ],
                 'autoneg': 'true',
                 'duplex': 'full',
                 'l1up': 'true',
                 'mac': data['macs'][iface],
                 'mtu': '1500',
                 'name': iface,
                 'speed': '1000',
                 'stats': get_net_stats(data, iface),
                 'up': 'true'
             }
      if iface == lan_if:
        net_entry['host_table'] = data['host_table']
      else:
        net_entry['gateways'] = [ data['ip'][iface]['gateway'] ]
        net_entry['nameservers'] = data['nameservers']
      network_table.append(net_entry)
    return network_table

def get_net_stats(data,iface):
    if_stat = data['ifstat'][iface]
    return {
                     'multicast': if_stat['rx_multicast'],
#                     'rx_bps': '342',
                     'rx_bytes': if_stat['rx_bytes'],
                     'rx_dropped': if_stat['rx_dropped'],
                     'rx_errors': if_stat['rx_errors'],
                     'rx_multicast': if_stat['rx_multicast'],
                     'rx_packets': if_stat['rx_packets'],
#                     'tx_bps': '250',
                     'tx_bytes': if_stat['tx_bytes'],
                     'tx_dropped': if_stat['tx_dropped'],
                     'tx_errors': if_stat['tx_errors'],
                     'tx_packets': if_stat['tx_packets']
           }
