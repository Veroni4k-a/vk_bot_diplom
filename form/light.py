from form.user_form import UserForm


class LightForm(UserForm):
    def __init__(self):
        super().__init__()
        self.light = None
        # Поле для породы собаки

    def set_light(self, light):
        self.light = light
        self.state = 'waiting_for_light'

    def is_light_completed(self):
        return all([self.full_name, self.phone, self.description, self.location, self.light])