from __future__ import print_function

import ftplib
import sys
import datetime
import re
import bisect
import zlib
import bintrees
from IPy import IP, IPSet

from .model import IPRange
from .utils import FixedOffset
from .parser import DelegatedParser

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

class Geolocator(object):
    def __init__(self, store):
        """Create a new Geolocator object using the specified store."""
        self.store = store

    def update(self):
        """Read the IP assignment data from AFRINIC, ARIN, APNIC, LACNIC
        and RIPE and store it in the store."""
        ranges = bintrees.FastRBTree()

        # Read all the delegate files
        ftp = ftplib.FTP('ftp.ripe.net')
        ftp.login()

        for registry in ['afrinic', 'arin', 'apnic', 'lacnic', 'ripencc']:
            parser = DelegatedParser(ranges)
            ftp.retrlines('RETR /pub/stats/%s/delegated-%s-extended-latest' \
                        % (registry, registry),
                        parser.got_line)

        ftp.quit()

        # Convert to list
        ranges = list(ranges.values())

        # Check for overlaps and emit warnings
        count = len(ranges)
        ndx = 0
        while ndx + 1 < count:
            e = ranges[ndx]
            n = ranges[ndx + 1]
            if n.startaddr <= e.endaddr and e.country != n.country:
                print('warning: fixed overlap %s, %s' % (e, n), file=sys.stderr)
                if e.endaddr > n.endaddr:
                    rest = Entry(IP(n.endaddr.int() + 1),
                                e.endaddr,
                                e.registry,
                                e.country)
                    ranges.insert(ndx + 2, rest)
                    count += 1
                e.endaddr = IP(n.startaddr.int() - 1)
            ndx += 1

        # Merge adjacent ranges with the same country code
        count = len(ranges)
        ndx = 0
        while ndx + 1 < count:
            if ranges[ndx + 1].country == ranges[ndx].country:
                ranges[ndx].endaddr = ranges[ndx + 1].endaddr
                del ranges[ndx + 1]
                count -= 1
            elif ranges[ndx + 1].startaddr == ranges[ndx].startaddr:
                print('warning: found conflict - %s, country %s/%s' \
                      % (ranges[ndx].startaddr, ranges[ndx].country,
                         ranges[ndx + 1].country), file=sys.stderr)
                del ranges[ndx + 1]
                count -= 1
            else:
                ndx += 1

        # Save the data
        self.store.save([IPRange(r.startaddr, r.country) for r in ranges])

        return len(ranges)

    def lookup(self, addr):
        """Lookup the specified address and return the IPRange object
        identifying its country and the start of the range.  The address may
        be either an IPy.IP object, or something that can be passed to the
        constructor of an IPy.IP object, for instance a string."""
        return self.store.lookup(addr)
