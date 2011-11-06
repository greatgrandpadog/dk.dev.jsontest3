

import re
from contextlib import closing
from sqlalchemy import *
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.dialects.mysql import *
from warnings import filterwarnings, resetwarnings
import MySQLdb ## only imported for warning suppression

class DataInterfaceObject(object):
    def __init__(self, db_host, db_user,db_password,db_name):
        self._db_host = db_host
        self._db_user = db_user
        self._db_password = db_password
        self._db_name = db_name
        self._db_engine_generic = None
        self._db_engine = None
        self._session_factory_generic = None
        self._session_factory = None
        self.CreateDatabaseEngines()
        
    def CreateDatabaseEngines(self):
        """Creates SqlAlchemy engines and connection."""     
        self._db_engine_generic = create_engine('mysql://' + self._db_user + ':' + self._db_password + '@' + self._db_host, pool_recycle=3600)
        self._session_factory_generic = sessionmaker(bind=self._db_engine_generic) 
        self._db_engine = create_engine('mysql://' + self._db_user + ':' + self._db_password + '@' + self._db_host + '/' + self._db_name, pool_recycle=3600)  
        self._session_factory = sessionmaker(bind=self._db_engine) 
 
    def ExcuteDBSQL(self, sql_text, given_connection = None):
        """Executes the given DB SQL statement."""
        if (given_connection != None):
            given_connection.execute(sql_text)
        else:
            with closing(self._db_engine.connect()) as connection:     
                connection.execute(sql_text)
       
    def ExcuteGenericSQL(self, sql_text, given_connection = None):
        """Executes the given Generic SQL statement."""
        if given_connection != None:
            given_connection.execute(sql_text) 
        else:
            with closing(self._db_engine_generic.connect()) as connection:     
                connection.execute(sql_text)
          
    def CreateDatabase(self, db_name, drop_first, connection = None):
        """Creates a database."""
        # Filter warnings here because mySQL will complain
        # if table does not exist on drop
        filterwarnings('ignore', category = MySQLdb.Warning)
        if drop_first:
            self.ExcuteGenericSQL('DROP DATABASE IF EXISTS ' + db_name, connection)    
        self.ExcuteGenericSQL('CREATE DATABASE IF NOT EXISTS ' + db_name, connection)
        resetwarnings()
        
    def CreateTables(self, db_connection, construct_tables, drop_first):
        """Creates tables in database for application."""   
        metadata = MetaData(db_connection)
        
        construct_tables(metadata)    
        
        #First, drop the tables if they already exist.
        if drop_first:
            metadata.drop_all()
        
        # Create the table.
        metadata.create_all()
        
    def CreateTableExplicitly(self, table_name, table_create_sql_text, drop_first, connection = None):
        """Creates the tables using explict SQL statement."""
        # Filter warnings here because mySQL will complain
        # if table does not exist on drop or exists on create
        filterwarnings('ignore', category = MySQLdb.Warning)
        if drop_first:
            self.ExcuteDBSQL('DROP TABLE IF EXISTS ' + table_name, connection)    
        self.ExcuteDBSQL(table_create_sql_text, connection)
        resetwarnings()

    def SetColumnComment(self, connection, table_name, column_name, column_def, comment):
        """Sets column comment in database"""    
        # Remove trailing comma if present
        match = re.match("(.+),", column_def, re.IGNORECASE)
        if match:
            column_def_mod = match.group(1)
        else:
            column_def_mod = column_def
        # Remove any existing comment part
        match = re.match("(.+)comment.+'.+'.*", column_def_mod, re.IGNORECASE)
        if match:
            column_def_mod = match.group(1)
        sql_text = 'ALTER TABLE `' + table_name + '` CHANGE COLUMN `' + column_name \
        + '` `' + column_name + '` ' + column_def_mod + ' comment ' + "'" + comment + "'"
        connection.execute(sql_text)
       
    def GetColumnDefinitionFromLine(self,line):
        """Gets a column name and definition from a text line if it contains a proper column definition."""
        match = re.match('`([\w.-]+)`(.+)', line.strip())
        if match:
            return True, match.group(1), match.group(2)
        else:
            return False, '', ''
        
    def GetColumnDefinitions(self, table_name):
        """Returns a dictionary of column names and their definitions for the given table name."""
        column_definitions = {};
        with closing(self._db_engine.connect()) as connection:     
            data = connection.execute('SHOW CREATE TABLE ' + table_name)  
            for row in data:
                for entry in row:
                    for line in entry.splitlines():
                        is_column_def, column_name, column_def = self.GetColumnDefinitionFromLine(line)
                        if is_column_def:
                            column_definitions[column_name] = column_def
            return column_definitions

    def AddCommentsToTable(self, connection, table_name, comment_dictionary):
        """Adds comments to columns in the given table."""
        #Since to my knowledge sqlalchemy table creation doesn't allow the inclusion of column comments,
        #comments are added here. They are added using ALTER TABLE MODIFY COLUMN.
        #This requires the entire column definition, which is obtained
        #using SHOW TABLE CREATE.
        column_defs = self.GetColumnDefinitions(table_name)
        for column_name, comment in comment_dictionary.iteritems():
            self.SetColumnComment(connection, table_name, column_name, column_defs[column_name], comment)

