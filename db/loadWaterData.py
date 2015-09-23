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

with open('../data/waterData.json') as data_file:
    waterData = json.load(data_file)
    waterData = byteify(waterData)

engine = create_engine("postgres://niallokane@localhost:5432/dev_waterweather")
metadata = MetaData(bind=engine)
Base = declarative_base()
measurement_id_seq = Sequence('measurement_id_seq')

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

class WaterBody(Base):
    __tablename__ = 'water_bodies'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    state_id = Column(Integer,ForeignKey('states.id'), primary_key=True)
    # county_id = Column(None, ForeignKey('counties.id'), primary_key=True)
    def __repr__(self):
       return "<WaterBody(id='%s', name='%s', state_id='%s')>" % (
                          self.id,  self.name, self.state_id)

class WaterMeasurement(Base):
    __tablename__ = 'water_measurements'

    value = Column(Float)
    measured_at = Column(DateTime)
    body_id = Column(BigInteger, ForeignKey('counties.id'), primary_key=True)

    def __repr__(self):
       return "<WaterMeasurement(value='%s', measured_at='%s', body_id='%s')>" % (
                          self.value, self.measured_at, self.body_id)

Sess = orm.sessionmaker(bind = engine)
session = Sess()

for body in waterData:
    currentBody = WaterBody(id=int(body['id']), name=body['name'], \
      state_id=int(body['stateId']))
    session.merge(currentBody)

session.commit()

for body in waterData:
    measurement = WaterMeasurement(value=body['value'], measured_at=body['dateTime'], body_id=int(body['id']))
    session.add(measurement)

session.commit()
