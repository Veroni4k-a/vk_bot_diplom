def save_to_db_dog(self, dog):
    """Save user data to the database"""
    insert_query = """
                 INSERT INTO dog_forms (full_name, phone, description,breed, latitude, longitude) 
                 VALUES (%s, %s, %s, %s, %s,%s);
             """

    latitude, longitude = map(float, dog.location)

    data_to_insert = (dog.full_name, dog.phone, dog.description, dog.breed,
                      latitude, longitude)

    # Execute insert query
    try:
        if self.cursor is not None:
            self.cursor.execute(insert_query, data_to_insert)
            self.connection.commit()
            print("Data saved successfully.")
        else:
            print("Cursor is not initialized.")
    except Exception as e:
        print(f"Error saving data: {e}")


def close_connection_dog(self):
    """Close database connection"""
    if self.cursor is not None:
        self.cursor.close()
    if self.connection is not None:
        self.connection.close()


def save_to_db(self, form):
    """Save user data to the database"""
    insert_query = """
           INSERT INTO user_forms (full_name, phone, description, latitude, longitude) 
           VALUES (%s, %s, %s, %s, %s);
       """

    latitude, longitude = map(float, form.location)

    data_to_insert = (form.full_name, form.phone, form.description,
                      latitude, longitude)

    # Execute insert query
    try:
        if self.cursor is not None:
            self.cursor.execute(insert_query, data_to_insert)
            self.connection.commit()
            print("Data saved successfully.")
        else:
            print("Cursor is not initialized.")
    except Exception as e:
        print(f"Error saving data: {e}")


def close_connection(self):
    """Close database connection"""
    if self.cursor is not None:
        self.cursor.close()
    if self.connection is not None:
        self.connection.close()


def save_to_db_rubbish(self, rubbish):
    """Save user data to the database"""
    insert_query = """
           INSERT INTO rubbish_forms (full_name, phone, description, latitude, longitude) 
           VALUES (%s, %s, %s, %s, %s);
       """

    latitude, longitude = map(float, rubbish.location)

    data_to_insert = (rubbish.full_name, rubbish.phone, rubbish.description,
                      latitude, longitude)

    # Execute insert query
    try:
        if self.cursor is not None:
            self.cursor.execute(insert_query, data_to_insert)
            self.connection.commit()
            print("Data saved successfully.")
        else:
            print("Cursor is not initialized.")
    except Exception as e:
        print(f"Error saving data: {e}")


def close_connection_rubbish(self):
    """Close database connection"""
    if self.cursor is not None:
        self.cursor.close()
    if self.connection is not None:
        self.connection.close()


# Форма с машинами заполнение в бд
def save_to_db_car(self, car):
    """Save user data to the database"""
    insert_query = """
           INSERT INTO car_forms (full_name, phone, description,number_avto, latitude, longitude) 
           VALUES (%s, %s, %s, %s, %s,%s);
       """

    latitude, longitude = map(float, car.location)

    data_to_insert = (car.full_name, car.phone, car.description, car.number,
                      latitude, longitude)

    # Execute insert query
    try:
        if self.cursor is not None:
            self.cursor.execute(insert_query, data_to_insert)
            self.connection.commit()
            print("Data saved successfully.")
        else:
            print("Cursor is not initialized.")
    except Exception as e:
        print(f"Error saving data: {e}")


def close_connection_car(self):
    """Close database connection"""
    if self.cursor is not None:
        self.cursor.close()
    if self.connection is not None:
        self.connection.close()


# Форма с проблемами по свету заполнение в бд

def save_to_db_light(self, light):
    """Save user data to the database"""
    insert_query = """
           INSERT INTO light_forms (full_name, phone, description,light, latitude, longitude) 
           VALUES (%s, %s, %s, %s, %s, %s);
       """

    latitude, longitude = map(float, light.location)

    data_to_insert = (light.full_name, light.phone, light.description, light.light,
                      latitude, longitude)

    # Execute insert query
    try:
        if self.cursor is not None:
            self.cursor.execute(insert_query, data_to_insert)
            self.connection.commit()
            print("Data saved successfully.")
        else:
            print("Cursor is not initialized.")
    except Exception as e:
        print(f"Error saving data: {e}")


def close_connection_light(self):
    """Close database connection"""
    if self.cursor is not None:
        self.cursor.close()
    if self.connection is not None:
        self.connection.close()


# Форма с светофором заполнение в бд
def save_to_db_traffic(self, traffic):
    """Save user data to the database"""
    insert_query = """
           INSERT INTO traffic_forms (full_name, phone, description, latitude, longitude) 
           VALUES (%s, %s, %s, %s, %s);
       """

    latitude, longitude = map(float, traffic.location)

    data_to_insert = (traffic.full_name, traffic.phone, traffic.description,
                      latitude, longitude)

    # Execute insert query
    try:
        if self.cursor is not None:
            self.cursor.execute(insert_query, data_to_insert)
            self.connection.commit()
            print("Data saved successfully.")
        else:
            print("Cursor is not initialized.")
    except Exception as e:
        print(f"Error saving data: {e}")


def close_connection_traffic(self):
    """Close database connection"""
    if self.cursor is not None:
        self.cursor.close()
    if self.connection is not None:
        self.connection.close()