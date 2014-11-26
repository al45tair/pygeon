from .utils import FixedOffset

import re
import datetime
from IPy import IP

class Entry(object):
    __slots__ = ['startaddr', 'endaddr', 'registry', 'country']
    def __init__(self, startaddr, endaddr, registry, country):
        self.startaddr = startaddr
        self.endaddr = endaddr
        self.registry = registry.lower()
        self.country = country.upper()

    def __cmp__(self, other):
        return cmp(self.startaddr, other.startaddr)

    def __eq__(self, other):
        return self.startaddr == other.startaddr

    def __hash__(self):
        return hash(self.startaddr)

    def __str__(self):
        return '%s-%s (%s) => %s' % (self.startaddr,
                                     self.endaddr,
                                     self.registry,
                                     self.country)

class DelegatedParser(object):
    # States
    START = 'START'
    RUNNING = 'RUNNING'
    
    def __init__(self, tree):
        self.state = DelegatedParser.START
        self.tree = tree
        
    def got_line(self, line):
        tree = self.tree
        
        line = line.strip()

        # Ignore comments and blank lines
        if line.startswith('#') or len(line) == 0:
            return

        fields = line.split('|')
        if self.state == DelegatedParser.START:
            self.version = fields[0]
            self.registry = fields[1]
            self.serial = fields[2]
            self.records = int(fields[3])

            m = re.match(r'([+-]?)(\d{2})(\d{2})', fields[6])
            offset = int(m.group(2)) * 60 + int(m.group(3))
            if m.group(1) == '-':
                offset = -offset

            self.tzinfo = FixedOffset(offset, fields[6])
            self.utcoffset = datetime.timedelta(minutes=offset)
            if not fields[4] or re.match(r'^0+$', fields[4]):
                self.startdate = None
            else:
                self.startdate = datetime.date(int(fields[4][:4]),
                                               int(fields[4][4:6]),
                                               int(fields[4][6:]))
            self.enddate = datetime.date(int(fields[5][:4]),
                                         int(fields[5][4:6]),
                                         int(fields[5][6:]))
            self.state = DelegatedParser.RUNNING
        elif self.state == DelegatedParser.RUNNING:
            if fields[5] == 'summary':
                return
            if fields[2] != 'ipv4' and fields[2] != 'ipv6':
                return
            if not fields[1].strip():
                return

            if fields[2] == 'ipv4':
                startaddr = IP(fields[3]).v46map()
                endaddr = IP(startaddr.int() + int(fields[4]) - 1).v46map()
                entry = Entry(startaddr, endaddr, fields[0], fields[1])
                tree[startaddr] = entry
            else:
                addr = IP('%s/%s' % (fields[3], fields[4]), make_net=True)
                startaddr = addr.net()
                endaddr = addr.broadcast()
                entry = Entry(startaddr, endaddr, fields[0], fields[1])
                tree[startaddr] = entry
