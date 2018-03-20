#!/usr/bin/python
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.util import quietRun
from mininet.log import setLogLevel, info
from mininet.term import makeTerms
from time import sleep
import os


class SimpleTopo(Topo):
    "Simple topology"

    def __init__(self):
        # Initialize topo
        Topo.__init__(self)

        # Add hosts and switch
        dhcp = self.addHost('h1')
        client = self.addHost('h2')

        switch = self.addSwitch('s1')

        # add link
        self.addLink(dhcp, switch)
        self.addLink(client, switch)


""" Several functions from dhcp demo"""
# DHCP server functions and data

DNSTemplate = """
start		10.0.0.10
end		10.0.0.90
option	subnet	255.255.255.0
option	domain	local
option	lease	7  # seconds
"""
# option dns 8.8.8.8
# interface h1-eth0


def makeDHCPconfig(filename, intf, gw, dns):
    "Create a DHCP configuration file"
    config = (
        'interface %s' % intf,
        DNSTemplate,
        'option router %s' % gw,
        'option dns %s' % dns,
        '')
    with open(filename, 'w') as f:
        f.write('\n'.join(config))


def startDHCPserver(host, gw, dns):
    "Start DHCP server on host with specified DNS server"
    info('* Starting DHCP server on', host, 'at', host.IP(), '\n')
    dhcpConfig = '/tmp/%s-udhcpd.conf' % host
    makeDHCPconfig(dhcpConfig, host.defaultIntf(), gw, dns)
    host.cmd('udhcpd -f', dhcpConfig,
             '1>/tmp/%s-dhcp.log 2>&1  &' % host)


def stopDHCPserver(host):
    "Stop DHCP server on host"
    info('* Stopping DHCP server on', host, 'at', host.IP(), '\n')
    host.cmd('kill %udhcpd')


# DHCP client functions

def startDHCPclient(host):
    "Start DHCP client on host"
    intf = host.defaultIntf()
    host.cmd('dhclient -v -d -r', intf)
    host.cmd('dhclient -v -d 1> /tmp/dhclient.log 2>&1', intf, '&')


def stopDHCPclient(host):
    host.cmd('kill %dhclient')


def waitForIP(host):
    "Wait for an IP address"
    info('*', host, 'waiting for IP address')
    while True:
        host.defaultIntf().updateIP()
        if host.IP():
            break
        info('.')
        sleep(1)
    info('\n')
    info('*', host, 'is now using',
         host.cmd('grep nameserver /etc/resolv.conf'))


if __name__ == '__main__':
    topo = SimpleTopo()
    net = Mininet(topo=topo, link=TCLink)
    dhcp, client = net.get('dhcp', 'client')
    # connectToInternet calls net.start() for us!
    startDHCPserver(dhcp, gw='10.0.1.222', dns='8.8.8.8')
    startDHCPclient(client)
    waitForIP(client)
