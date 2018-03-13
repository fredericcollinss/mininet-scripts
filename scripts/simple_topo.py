#!/usr/bin/python
from mininet.topo import Topo

class SimpleTopo(Topo):
    def __init__(self, *args, **kwargs):
        Topo.__init__(self, *args, **kwargs)
        dhcp = self.addHost('h1', ip='10.0.0.10/24')