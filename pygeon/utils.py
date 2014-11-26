import datetime

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
