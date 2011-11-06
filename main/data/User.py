

class User(object):
    def __init__(self, name, age, password):
        self.name = name
        self.age = age
        self.password = password

    def __repr__(self):
        return "<User('%s','%s','%s','%s')>" % (self.user_id, self.name, self.age, self.password)
        
