

import uuid
from contextlib import closing
from sqlalchemy import *
from sqlalchemy.orm import mapper, class_mapper
from sqlalchemy.orm.exc import UnmappedClassError
from sqlalchemy.dialects.mysql import *

#Add to path to facilitate importing modules from other folders.
import os, sys
sys.path.append(os.path.join(os.path.dirname( __file__ ),'../framework'))

from User import *
from State import *
from DataInterfaceObject import *

class StateDataUtils(DataInterfaceObject):
    def __init__(self, db_host, db_user, db_password, db_name):
        super(StateDataUtils, self).__init__(db_host, db_user, db_password, db_name)
        self._states_table_name = "states"   
        self._states_column_name_id = 'id'
        self._states_column_name_name = 'name'
        self._states_column_name_abbreviation = 'abbreviation'
        self._states_column_name_counties = 'counties'           
        self._states_table = None
        
    def ConstructStatesTable(self, metadata):
        """Construct sqlalchemy table objects. Called by base class CreateTables() method."""
        default_table_options = { u'mysql_engine': u'InnoDB', u'mysql_default charset': u'utf8', u'mysql_collate': u'utf8_unicode_ci'}        
               
        self._states_table = Table(self._states_table_name, metadata,
            Column(self._states_column_name_id, CHAR(36), primary_key=True),
            Column(self._states_column_name_name, String(50)),
            Column(self._states_column_name_abbreviation, CHAR(2)),
            Column(self._states_column_name_counties, MEDIUMTEXT)
            , **default_table_options)
        self._states_table.create()       
             
    def CreateStatesTableExplicitly(self, connection):
        """Creates the states table using explict SQL statement."""
        self.CreateTableExplicitly(self._states_table_name,
                            "CREATE TABLE IF NOT EXISTS `states` (`id` char(36) NOT NULL comment 'should be a uuid',"
                            + "`name` varchar(50) default NULL comment 'should be the state name',"
                            + "`abbreviation` char(2) default NULL comment 'should be the state abbreviation',"
                            + "`counties` mediumtext comment 'should be a JSON string',"
                            + "PRIMARY KEY  (`id`)"
                            + ") ENGINE=InnoDB DEFAULT CHARSET=utf8", True, connection)     
      
    def AddCommentsToStatesTable(self, connection, prefix):
        """Adds comments to columns in the states table."""
        self.AddCommentsToTable(connection, self._states_table_name,
            {self._states_column_name_id: 'should be a uuid',
            self._states_column_name_name: 'should be the state name',
            self._states_column_name_abbreviation: 'should be the state abbreviation',
            self._states_column_name_counties: 'should be a JSON string'})
        
    def MapStatesTable(self):
        """Maps states table to States class for County application."""
        if self._states_table == None:
            with closing(self._db_engine.connect()) as connection:
                metadata = MetaData(connection)
                #Presuming that states table has already been created explicity SQL and SqlAlchemy reflection.
                self._states_table = Table(self._states_table_name, metadata, autoload=True)
        try:
            class_mapper(State)
        except UnmappedClassError:
            mapper(State, self._states_table)            
                    
    def AddStateRecord(self, json_string, json_object):
        with closing(self._session_factory()) as session:            
            a_state = State(uuid.uuid1(), json_object[0]['state_name'], json_object[0]['state_abbreviation'], json_string)     
            session.add(a_state)
            session.commit()
            
    def GetAllStateRecords(self):
        self.MapStatesTable()
        with closing(self._session_factory()) as session: 
            return session.query(State).order_by(State.id)           
            
    def GetStateRecord(self, state_name):
        self.MapStatesTable()
        with closing(self._session_factory()) as session:
            records = session.query(State).filter(State.name==state_name).order_by(State.id).all()
            if len(records) > 0:
                return records[0]
            else:
                return None
        
        
        
        
        
        
        



                


