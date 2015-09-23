from sqlalchemy import *

engine = create_engine(
    "postgres://niallokane@localhost:5432/dev_waterweather",
    isolation_level="READ UNCOMMITTED"
)

metadata = MetaData()
measurement_id_seq = Sequence('measurement_id_seq')

states_table = Table('states', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(40)),
    Column('abbr', String(5))
)
 
counties_table = Table('counties', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100)),
    Column('state_id', None, ForeignKey('states.id'))
)
 
bodies_tables = Table('water_bodies', metadata,
    Column('id', BigInteger, primary_key=True),
    Column('name', String),
    Column('state_id', Integer, ForeignKey('states.id'), nullable=False)
)

measurements_table = Table('water_measurements', metadata,
    Column('id', Integer, measurement_id_seq, server_default=measurement_id_seq.next_value(), primary_key=True),
    Column('value', Float),
    Column('measured_at', DateTime),
    Column('body_id', BigInteger, ForeignKey("water_bodies.id")),
)

# create tables in database
metadata.create_all(engine)
