
import urllib2
import simplejson

class CountyDataRetriever:
    def __init__(self):
        self._state_abbreviations = {"VERMONT": "VT", "GEORGIA": "GA", "IOWA":"IA",
                               "Armed Forces Pacific": "AP", "GUAM": "GU", "KANSAS": "KS",
                               "FLORIDA": "FL", "AMERICAN SAMOA": "AS",
                               "NORTH CAROLINA": "NC", "HAWAII": "HI",
                               "NEW YORK": "NY", "CALIFORNIA": "CA",
                               "ALABAMA": "AL", "IDAHO": "ID",
                               "FEDERATED STATES OF MICRONESIA": "FM",
                               "Armed Forces Americas": "AA", "DELAWARE": "DE",
                               "ALASKA": "AK", "ILLINOIS": "IL",
                               "Armed Forces Africa": "AE", "SOUTH DAKOTA": "SD",
                               "CONNECTICUT": "CT", "MONTANA": "MT",
                               "MASSACHUSETTS": "MA", "PUERTO RICO": "PR",
                               "Armed Forces Canada": "AE", "NEW HAMPSHIRE": "NH",
                               "MARYLAND": "MD", "NEW MEXICO": "NM",
                               "MISSISSIPPI": "MS", "TENNESSEE": "TN",
                               "PALAU": "PW", "COLORADO": "CO",
                               "Armed Forces Middle East": "AE",
                               "NEW JERSEY": "NJ", "UTAH": "UT",
                               "MICHIGAN": "MI", "WEST VIRGINIA": "WV",
                               "WASHINGTON": "WA", "MINNESOTA": "MN",
                               "OREGON": "OR", "VIRGINIA": "VA",
                               "VIRGIN ISLANDS": "VI", "MARSHALL ISLANDS": "MH",
                               "WYOMING": "WY", "OHIO": "OH", "SOUTH CAROLINA": "SC",
                               "INDIANA": "IN", "NEVADA": "NV", "LOUISIANA": "LA",
                               "NORTHERN MARIANA ISLANDS": "MP", "NEBRASKA": "NE",
                               "ARIZONA": "AZ", "WISCONSIN": "WI",
                               "NORTH DAKOTA": "ND", "Armed Forces Europe": "AE",
                               "PENNSYLVANIA": "PA", "OKLAHOMA": "OK",
                               "KENTUCKY": "KY", "RHODE ISLAND": "RI",
                               "DISTRICT OF COLUMBIA": "DC", "ARKANSAS": "AR",
                               "MISSOURI": "MO", "TEXAS": "TX", "MAINE": "ME"}

    def GetAbbreviation(self,state):
        """Get a state abbreviation"""
        state_upper = state.upper()
        if state_upper in self._state_abbreviations:
            return self._state_abbreviations[state_upper]
        else:
            return ""
        
    def GetCountyDataUrl(self, state):
        """Get the url to use in order to retriev json data for a given state."""
        state_abbreviation = self.GetAbbreviation(state)
        if state_abbreviation is not None and len(state_abbreviation) > 0:
            return "http://api.sba.gov/geodata/county_data_for_state_of/" + state_abbreviation + ".json"
        else:
            return "";
        
    def GetJsonDataFromString(self, json_string):
        """Get JSON data object from JSON string."""
        return simplejson.loads(json_string)
        
    def GetJsonString(self,state):
        """Get JSON string for the given state."""
        data_url = self.GetCountyDataUrl(state)
        if data_url is not None and len(data_url) > 0:
            req = urllib2.Request(self.GetCountyDataUrl(state), None, {'user-agent':'syncstream/vimeo'})
            opener = urllib2.build_opener()
            f = opener.open(req)
            json_string = f.read()
            return json_string
        else:
            return ""
        
    def GetJsonStringAndObject(self,state):
        """Get the JSON string and object for the given state."""
        json_string = self.GetJsonString(state)
        if json_string is not None and len(json_string) > 0:
            json_object = simplejson.loads(json_string)
            return json_string, json_object
        else:
            return "",""
        
    def GetJsonObject(self,state):
        """Get the JSON object for the given state."""
        json_string = self.GetJsonString(state)
        if json_string is not None and len(json_string) > 0:
            json_object = simplejson.loads(json_string)
            return json_object
        else:
            return ""       


