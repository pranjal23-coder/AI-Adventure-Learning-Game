from db import connection

class AIRecommendationModel:
    def __init__(self, connection):
        self.connection=connection

    def save_recommendation(self, user_id, recommendation):

        cursor = self.connection.cursor()

        query = """
        INSERT INTO ai_recommendation
        (user_id, recommendation)
        VALUES(%s, %s)
        """

        values = (
            user_id,
            recommendation
        )

        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()


    def get_recommendation(self, user_id):

        cursor =self.connection.cursor(dictionary=True)

        query=(
            """
            SELECT * FROM ai_recommendation
            WHERE user_id=%s
            order by id desc
            limit 1
            """
        )
        cursor.execute(query, (user_id,))
        result=cursor.fetchone()
        cursor.close()
        

        return result


    def update_recommendation(self, user_id, recommendation):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE AI_recommendation
            SET recommendation=%s
            WHERE user_id=%s
            """,
            (recommendation, user_id)
        )
             
        connection.commit()


    def delete_recommendation(self, user_id):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE FROM AI_recommendation
            WHERE user_id=%s
            """,
            (user_id,)
        )

        connection.commit()
        
    def get_latest_recommendation(self, user_id):
    
            cursor = self.connection.cursor(dictionary=True)
    
            query=(
                """
                SELECT recommendation
                from ai_recommendation
                WHERE user_id=%s
                order by created_at desc
                limit 1
                """
            )
            cursor.execute(query, (user_id,))
            result=cursor.fetchone()
            cursor.close()
            
            if result:
                return result["recommendation"]
            
    
            return None    