#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink

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

if __name__ == '__main__':
    topo = SimpleTopo()
    net = Mininet( topo=topo, link=TCLink )
    dhcp, client = net.get('dhcp', 'client')

    