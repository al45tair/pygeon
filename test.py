# A *very* simple and very basic test script

import pygeon

store = pygeon.SQLAlchemyStore('sqlite:////tmp/ipranges.sqlite3')

geo = pygeon.Geolocator(store)

geo.update()

iprange = geo.lookup('216.58.208.46')
