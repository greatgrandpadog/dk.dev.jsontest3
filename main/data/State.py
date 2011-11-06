

class State(object):
    def __init__(self, id, name, abbreviation, counties):
        self.id = id
        self.name = name
        self.abbreviation = abbreviation
        self.counties = counties

    def __repr__(self):
        return "<State('%s','%s','%s','%s')>" % (self.id, self.name, self.abbreviation, self.counties)
        
