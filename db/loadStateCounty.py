from sqlalchemy import *
import sqlalchemy.orm as orm
import json
from sqlalchemy.ext.declarative import declarative_base

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
Base = declarative_base()

class State(Base):
    __tablename__ = 'states'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbr = Column(String)

    def __repr__(self):
       return "<State(id='%s', name='%s', abbr='%s')>" % (
                          self.id,  self.name, self.abbr)

class County(Base):
    __tablename__ = 'counties'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    state_id = Column(Integer, ForeignKey('states.id'), nullable=False)

    def __repr__(self):
       return "<County(id='%s', name='%s', state_id='%s')>" % (
                          self.id,  self.name, self.state_id)

Sess = orm.sessionmaker(bind = engine)
session = Sess()

for state in stateData:
    currentState = State(id=int(state), name=stateData[state]['name'], abbr=stateData[state]['abbreviation'])
    session.merge(currentState)

session.commit()

for county in countyData:
    currentCounty = County(id=int(county), name=countyData[county]['county'], state_id=int(countyData[county]['stateId']))
    session.merge(currentCounty)

session.commit()
