class UserForm:
    def __init__(self):
        self.full_name = None
        self.phone = None
        self.description = None
        self.location = None
        self.state = 'waiting_for_full_name'

    def set_full_name(self, full_name):
        self.full_name = full_name
        self.state = 'waiting_for_phone'

    def set_phone(self, phone):
        self.phone = phone
        self.state = 'waiting_for_description'

    def set_description(self, description):
        self.description = description
        self.state = 'waiting_for_location'

    def set_location(self, latitude, longitude):
        self.location = latitude,longitude
        self.state = 'waiting_for_completed'


    def is_completed(self):
        return all([self.full_name, self.phone, self.description, self.location])


