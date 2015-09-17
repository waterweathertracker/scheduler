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

with open('../data/fips_countyCd_detailed.json') as data_file:
    countyData = json.load(data_file)
    countyData = byteify(countyData)

engine = create_engine("postgres://niallokane@localhost:5432/dev_waterweather")
metadata = MetaData(bind=engine)

tableStates = Table('states', metadata, autoload=True)
tableCounties = Table('counties', metadata, autoload=True)

class Row(object):
    pass

rowmapper = orm.Mapper(Row,tableStates)

Sess = orm.sessionmaker(bind = engine)
session = Sess()

for state in stateData:
    row1 = Row()
    row1.id = int(state)
    row1.name = stateData[state]['name']
    row1.abbr = stateData[state]['abbreviation']
    session.add(row1)

session.commit()
orm.clear_mappers()
rowmapper = orm.Mapper(Row, tableCounties)

Sess = orm.sessionmaker(bind = engine)
session = Sess()

for county in countyData:
    row1 = Row() 
    row1.id = int(county)
    row1.name = countyData[county]['county']
    row1.state_id = int(countyData[county]['stateId'])
    session.add(row1)

session.commit()
