__author__ = 'thihara'

from dbutil import DBUtil
from werkzeug.security import generate_password_hash, check_password_hash

"""
    Class handling service and data layer logical operations on users.
"""
class UserService:

    dbutil = DBUtil()
    dbcon = None

    # Returns a database connection. Obtains a new database connection if one isn't already set.
    def get_db(self):
        if self.dbcon is None:
            self.dbcon = self.dbutil.connect_db()

        return self.dbcon

    # Hashes the password with MD5 algorithm along with a salt of length 8
    def get_salted_md5_hash(self, password):
        return generate_password_hash(password, 'md5', 8)

    """
    Checks a username and password against the database.
    Returns
        True : If a user by the passed username exist and the given password matches the user's password in the database.
        False : If a user doesn't exist in the database, or if the password given doesn't match the user's password in the database.
    """
    def validate_credentials(self, username, password):
        user_list = self.get_db().execute('select * from users where username=?', [username]).fetchall()

        if len(user_list) < 1:
            return False
        else:
            return check_password_hash(user_list[0][2], password)

    # Save user details into the database
    def save_user(self, username, fullname, password):
        self.get_db().execute('insert into users(username,fullname,password) values(?,?,?)',
                              [username, fullname, self.get_salted_md5_hash(password)])

        self.get_db().commit()

    """
    Checks if a user with the same username already exist in the database.
    Returns True : If the user exists in the database. False: If the user doesn't exist in the database.
    """
    def does_user_exist(self, username):
        user_list = self.get_db().execute('select * from users where username=?', [username]).fetchall()

        if len(user_list) > 0:
            return True
        else:
            return False

    # Returns all the users currently in the database
    def get_users(self):
        return self.get_db().execute('select fullname, username from users').fetchall()

    """
    Registers a new user. Checks if the given two passwords match, and whether a user by the same username already exists
    prior to persisting the details into the database.

    Returns
        None : Ff there are no errors and the data was persisted.
        Error Message : If there was an error, the error message is returned and no data is persisted.
    """
    def register_user(self, fullname, username, password, confirm_password):
        error = None

        if password != confirm_password:
            error = "Both passwords must match"
        elif self.does_user_exist(username):
            error = "Username already exist"
        else:
            self.save_user(username, fullname, password)

        return error