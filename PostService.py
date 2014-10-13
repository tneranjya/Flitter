__author__ = 'thihara'

from dbutil import DBUtil

"""
    Class handling service and data layer operations on posts.
"""
class PostService:

    dbutil = DBUtil()
    dbcon = None

    # Returns a database connection. Obtains a new database connection if one isn't already set.
    def get_db(self):
        if self.dbcon is None:
            self.dbcon = self.dbutil.connect_db()

        return self.dbcon

    #Returns all posts created by the user with the given username.
    def get_posts_by_user(self, username):
        posts = self.get_db().execute('select post_content,posted_timestamp,posted_by from '
                                      'posts where posted_by=? order by posted_timestamp DESC ', [username]).fetchall()

        return posts

    #Saves a post created by a user.
    def save_post(self, posted_user, post_content):
        self.get_db().execute('insert into posts(posted_by,post_content) values(?,?)', [posted_user, post_content])
        self.get_db().commit()
