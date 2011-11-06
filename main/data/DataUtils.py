

from contextlib import closing
from sqlalchemy import *
from sqlalchemy.orm import mapper, sessionmaker

#Add to path to facilitate importing modules from other folders.
import os, sys
sys.path.append(os.path.join(os.path.dirname( __file__ ),'../framework'))

from User import *
from State import *
from StateDataUtils import *
from DataInterfaceObject import *

class DataUtils(DataInterfaceObject):
    def __init__(self):
        super(DataUtils, self).__init__("localhost", "webuser", "webuser", "County1")     
        self._states_utils = StateDataUtils(self._db_host, self._db_user, self._db_password, self._db_name)    
                   
    def InitializeDatabase(self, use_explicit_table_creation_and_reflection = False):
        """Initializes database for County application."""
        self.CreateDatabase(self._db_name, True)           
        with closing(self._db_engine.connect()) as connection:
            metadata = MetaData(connection)
            # Experimenting with two different ways of creating the states table.
            #       1) Create table using explicit SQL then use SqlAlchemy reflection.
            # or    2) Create table via SqlAlchemy then add column comments that SqlAlchemy doesn't create. 
            if use_explicit_table_creation_and_reflection:
                self._states_utils.CreateStatesTableExplicitly(connection)
                #States table has already been created explicity SQL and SqlAlchemy reflection.
                self._states_utils._states_table = Table(self._states_utils._states_table_name, metadata, autoload=True)
            else:
                #Create states table using SqlAlchemy Table() and Column() methods.
                self.CreateTables(connection, self._states_utils.ConstructStatesTable, True)
                ##Add comments to columns
                self._states_utils.AddCommentsToStatesTable(connection, "")
        self.MapTables()
            
    def MapTables(self):
        self._states_utils.MapStatesTable()

    def AddStateRecord(self, json_string, json_object):
        self.MapTables()
        self._states_utils.AddStateRecord(json_string, json_object)
        
    def GetAllStateRecords(self):
        self.MapTables()
        return self._states_utils.GetAllStateRecords()
        
    def GetStateRecord(self, state_name):
        self.MapTables()
        return self._states_utils.GetStateRecord(state_name)
        
        
        
        
        



                

