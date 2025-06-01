from form.user_form import UserForm


class CarForm(UserForm):
    def __init__(self):
        super().__init__()
        self.number = None


    def set_number(self, number):
        self.number = number
        self.state = 'waiting_for_number'

    def is_car_completed(self):
        return all([self.full_name, self.phone, self.description, self.location, self.number])