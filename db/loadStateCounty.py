from sqlalchemy import *
import sqlalchemy.orm as orm
import json

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

with open('../data/fips_stateCd.json') as data_file: 
    stateData = json.load(data_file)
    stateData = byteify(stateData)


engine = create_engine("postgres://niallokane@localhost:5432/dev_waterweather")
metadata = MetaData(bind=engine)

table = Table('states', metadata, autoload=True)

class Row(object):
    pass
rowmapper = orm.Mapper(Row,table)
print table.columns


Sess = orm.sessionmaker(bind = engine)
session = Sess()

for state in stateData:
    row1 = Row() 
    row1.id = int(state)
    row1.name = stateData[state]['name']
    row1.abbr = stateData[state]['abbreviation']
    session.add(row1)

session.commit()
