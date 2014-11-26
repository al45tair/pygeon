class IPRange(object):
    def __init__(self, start, country):
        #: The first IP address in the range
        self.start = start

        #: The country code
        self.country = country

    def __repr__(self):
        return 'IPRange(%r, %r)' % (self.start, self.country)
    
