import datetime
import IPy
from IPy import IP

# Monkeypatch IPy so it works on Python 3
def _ip_lt(self, other):
    return self.__cmp__(other) < 0
def _ip_le(self, other):
    return self.__cmp__(other) <= 0
def _ip_ge(self, other):
    return self.__cmp__(other) >= 0
def _ip_gt(self, other):
    return self.__cmp__(other) > 0

IP.__lt__ = _ip_lt
IP.__le__ = _ip_le
IP.__ge__ = _ip_ge
IP.__gt__ = _ip_gt
    
class Entry(object):
    __slots__ = ['startaddr', 'endaddr', 'registry', 'country']
    def __init__(self, startaddr, endaddr, registry, country):
        self.startaddr = startaddr
        self.endaddr = endaddr
        self.registry = registry.lower()
        self.country = country.upper()

    def __cmp__(self, other):
        return self.startaddr.__cmp__(other.startaddr)

    def __lt__(self, other):
        return self.startaddr < other.startaddr
    def __le__(self, other):
        return self.startaddr <= other.startaddr
    def __eq__(self, other):
        return self.startaddr == other.startaddr
    def __ge__(self, other):
        return self.startaddr >= other.startaddr
    def __gt__(self, other):
        return self.startaddr > other.startaddr
    
    def __hash__(self):
        return hash(self.startaddr)

    def __str__(self):
        return '%s-%s (%s) => %s' % (self.startaddr,
                                     self.endaddr,
                                     self.registry,
                                     self.country)

class FixedOffset(datetime.tzinfo):
    """Represents a time zone with a simple fixed offset from UTC."""
    
    ZERO = datetime.timedelta(0)

    def __init__(self, offset, name):
        self.__offset = datetime.timedelta(minutes=offset)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return FixedOffset.ZERO
