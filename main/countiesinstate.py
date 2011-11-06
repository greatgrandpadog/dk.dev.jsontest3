
import json

#Add to path to facilitate importing modules from other folders.
import os, sys
sys.path.append(os.path.join(os.path.dirname( __file__ ),'data'))
from DataUtils import DataUtils


class countiesinstate:
    def GET(self, state_name):
        data_utils = DataUtils()
        state_record = data_utils.GetStateRecord(state_name)
        if state_record != None:
            response_string = state_record.counties
        else:
            response_string = json.dumps([])   

        return response_string
