

import CountyDataRetriever

#Add to path to facilitate importing modules from other folders.
import os, sys
sys.path.append(os.path.join(os.path.dirname( __file__ ),'../data'))

from DataUtils import *
        
if __name__=="__main__":
    "Program to initialize database for County1 application."
    
    print "Initializing database..."
    data_utils = DataUtils()
    data_utils.InitializeDatabase()
  
    data_retriever = CountyDataRetriever.CountyDataRetriever()

    print "Adding data for Kansas..."
    json_string, json_object = data_retriever.GetJsonStringAndObject("Kansas")   
    data_utils.AddStateRecord(json_string, json_object)
 
    print "Adding data for Missouri..."   
    json_string, json_object = data_retriever.GetJsonStringAndObject("Missouri")  
    data_utils.AddStateRecord(json_string, json_object)
    print "Done."
    
    state_records = data_utils.GetAllStateRecords()
    for instance in state_records:
        print "Name: %s; Abbrev: %s; Counties: %s" % (instance.name, instance.abbreviation, "<counties>")  
    print "Beyond done."
    
    state_name = 'Kansas'
    state_record = data_utils.GetStateRecord(state_name)
    print state_name + "info:"
    if state_record != None:
        print "Name: %s; Abbrev: %s; Id: %s; Counties: %s" % (state_record.name, state_record.abbreviation, state_record.id, "<counties>")
    else:
        print "No record for " + state_name
  
    state_name = 'Missouri'
    state_record = data_utils.GetStateRecord(state_name)
    print state_name + "info:"
    if state_record != None:
        print "Name: %s; Abbrev: %s; Id: %s; Counties: %s" % (state_record.name, state_record.abbreviation, state_record.id, "<counties>")
    else:
        print "No record for " + state_name
     
    print "Beyond beyond done."
        
    