
class UsersModel:

    def __init__(self, connection):
        self.connection = connection


    def create_user(self, fullname, username, email, password):

        cursor = self.connection.cursor()

        query = """
            INSERT INTO Users
            (fullname, username, email, password)
            VALUES (%s, %s, %s, %s)
        """

        values = (
            fullname,
            username,
            email,
            password
        )

        cursor.execute(query, values)

        self.connection.commit()

        user_id = cursor.lastrowid

        cursor.close()

        return user_id


    def login_user(self, username, password):

        cursor = self.connection.cursor(dictionary=True)

        try:

            query = """
                SELECT *
                FROM Users
                WHERE (username = %s OR email = %s)
                AND password = %s
                limit 1
            """

            values = (
                username,
                username,
                password
            )

            cursor.execute(query, values)

            user = cursor.fetchone()

            return user

        finally:
            cursor.fetchall()

            cursor.close()

    def get_user(self, user_id):

        cursor = self.connection.cursor(dictionary=True)

        try:

            sql = """
                SELECT *
                FROM Users
                WHERE user_id = %s
            """

            cursor.execute(sql, (user_id,))

            return cursor.fetchone()

        finally:

            cursor.close()

    def update_user(
        self,
        user_id,
        fullname,
        username,
        email
    ):

        cursor = self.connection.cursor()

        try:

            sql = """
                UPDATE Users
                SET
                    fullname = %s,
                    username = %s,
                    email = %s
                WHERE user_id = %s
            """

            values = (
                fullname,
                username,
                email,
                user_id
            )

            cursor.execute(sql, values)

            self.connection.commit()

        finally:

            cursor.close()


    def delete_user(self, user_id):

        cursor = self.connection.cursor()

        try:

            sql = """
                DELETE FROM Users
                WHERE user_id = %s
            """

            cursor.execute(sql, (user_id,))

            self.connection.commit()

        finally:

            cursor.close()
            