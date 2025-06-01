from  form.user_form import UserForm
class DogForm(UserForm):
    def __init__(self):
        super().__init__()
        self.breed = None
        self.photo_path = None

    # Поле для породы собаки

    def set_breed(self, breed):
        self.breed = breed
        self.state = 'waiting_for_breed'

    def set_photo(self, photo_path):
        self.photo_path = photo_path


    def is_dog_completed(self):
        return all([self.full_name, self.phone, self.description,self.breed, self.location])