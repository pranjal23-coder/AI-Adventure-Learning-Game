from db import connection


class LeaderboardModel:
    def __init__(self, connection):
            self.connection = connection

    def update_score(self, user_id, score):

        cursor = connection.cursor()

        query = """
            UPDATE Leaderboard
            SET total_score = total_score + %s
            WHERE user_id = %s
        """

        cursor.execute(query, (score, user_id))

        connection.commit()

        cursor.close()


    def update_ranks(self):

        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT id
            FROM Leaderboard
            ORDER BY total_score DESC
        """

        cursor.execute(query)

        players = cursor.fetchall()

        for position, player in enumerate(players, start=1):

            update_query = """
                UPDATE Leaderboard
                SET rank_position = %s
                WHERE id = %s
            """

            cursor.execute(
                update_query,
                (position, player["id"])
            )

        connection.commit()

        cursor.close()


    def get_leaderboard(self):

        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                l.id,
                l.user_id,
                u.username,
                l.total_score,
                l.rank_position
            FROM Leaderboard l
            INNER JOIN Users u
                ON l.user_id = u.user_id
            ORDER BY l.total_score DESC
        """

        cursor.execute(query)

        leaderboard = cursor.fetchall()

        cursor.close()

        return leaderboard
    
    
    def add_score(self, user_id, score):
        
        
        cursor = self.connection.cursor()


        cursor.execute(
        """
        SELECT total_score
        FROM Leaderboard
        WHERE user_id = %s
        """,
        (user_id,)
    )
        row = cursor.fetchone()
        if row:
            new_score = row[0] + score
            
            cursor.execute(
            """
            UPDATE Leaderboard
            SET total_score = %s
            WHERE user_id = %s
            """,
            (new_score, user_id)
            
           )
            

        else:
            cursor.execute(
        """
        insert into LeaderBoard
        (user_id, total_score, rank_position)
        values(%s,%s,%s)
        """,
        (user_id, score, 0)
            )
            
        self.connection.commit()
        cursor.close()
        
    def update_ranks(self):
        cursor = self.connection.cursor()
        cursor.execute(
        """
        SELECT id
        FROM Leaderboard
        ORDER BY total_score DESC
        """
    )
        
        rows = cursor.fetchall()

        rank = 1

        for row in rows:

          cursor.execute(
            """
            UPDATE Leaderboard
            SET rank_position = %s
            WHERE id = %s
            """,
            (rank, row[0])
        )

        rank += 1
        self.connection.commit()
        cursor.close()    
        
        
    def create_leaderboard(self, user_id, total_score=0, rank_position=0):

       cursor = self.connection.cursor()

       query = """
        INSERT INTO leaderboard
        (user_id, total_score, rank_position)
        VALUES (%s, %s, %s)
        """

       cursor.execute(
        query,
        (user_id, total_score, rank_position)
        )

       self.connection.commit()
       cursor.close()    