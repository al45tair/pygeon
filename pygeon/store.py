from IPy import IP
from .model import IPRange

class Store(object):
    def save(self, ranges):
        """Save the given ranges in the store.  The new ranges should
        *replace* any existing ranges."""
        raise NotImplementedError('You must implement save')

    def lookup(self, addr):
        """Return an IPRange given an address.  Returns None if no range
        covers the given address."""
        raise NotImplementedError('You must implement lookup')
    
class SQLAlchemyStore(Store):
    """An IP range store based on SQLAlchemy.  You can create this from an
    SQLAlchemy Engine or Connection object, or by specifying a connection
    string URL."""
    
    def __init__(self, ecu):
        """Construct an SQLAlchemyStore given an Engine or a Connection, or
        a connection string URL."""
        
        from sqlalchemy import create_engine
        from sqlalchemy.engine import Engine, Connection

        self.connection = None
        self.owns_connection = True
        self.metadata = None
        self.table = None
        
        if isinstance(ecu, Engine):
            self.engine = ecu
        elif isinstance(ecu, Connection):
            self.engine = ecu.engine
            self.connection = ecu
            self.owns_connection = False
        else:
            self.engine = create_engine(ecu)

    def _connect(self):
        if self.connection:
            return self.connection
        self.connection = self.engine.connect()
        return self.connection
    
    def _disconnect(self):
        if self.owns_connection:
            self.connection.close()
            self.connection = None

    def _table(self):
        from sqlalchemy import MetaData, Table, Column, String, CHAR

        if self.table is None:
            self.metadata = MetaData()

            self.table = Table('pygeon_ranges', self.metadata,
                               Column('start', String(32), primary_key=True),
                               Column('country', CHAR(2), nullable=False))

            self.table.create(self.engine, checkfirst=True)
            
        return self.table

    def save(self, ranges):
        """Save the specified list of IPRanges to the SQLAlchemy store."""
        def pad(h):
            return '0'*(32 - len(h)) + h
        
        tbl = self._table()
        conn = self._connect()
        try:
            def padhex(ip):
                h = ip.strHex()[2:]
                return '0' * (32 - len(h)) + h
                
            with conn.begin() as trans:
                conn.execute(tbl.delete())
                conn.execute(tbl.insert(),
                              *[{ 'start': padhex(r.start),
                                  'country': r.country } for r in ranges])
        finally:
            self._disconnect()

    def lookup(self, addr):
        """Given an address, locate it in the store and return an IPRange."""
        from sqlalchemy.sql import select
        
        ipaddr = IP(addr)
        if ipaddr.version() == 4:
            ipaddr = ipaddr.v46map()

        h = ipaddr.strHex()[2:]
        h = '0'*(32 - len(h)) + h

        tbl = self._table()
        conn = self._connect()
        try:
            with conn.begin() as trans:
                stmt = select([tbl]).where(tbl.c.start <= h)\
                  .order_by(tbl.c.start.desc()).limit(1)
                result = conn.execute(stmt).fetchone()
                if result:
                    h = result['start']
                    ipaddr = IP('0x' + h)
                    
                    try:
                        ipaddr = ipaddr.v46map()
                    except ValueError:
                        pass
                    
                    return IPRange(ipaddr, result['country'])
            return None
        finally:
            self._disconnect()
