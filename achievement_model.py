class AchievementModel:

    def __init__(self, connection):
        self.connection = connection

    def get_achievement(self, user_id):

        cursor = self.connection.cursor(dictionary=True)
        
        try:
            

            cursor.execute("""
                SELECT
                id,
                user_id,
                badges,
                stars,
                certificates,
                total_xp,
                unlocked_title
                FROM achievement
                WHERE user_id = %s
                """, (user_id,))
           
            return cursor.fetchone()
       
        finally:
            cursor.close()
