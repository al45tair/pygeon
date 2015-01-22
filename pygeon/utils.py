import datetime

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
