class ProgressModel:

    def __init__(self, connection):
        self.connection = connection


    def create_progress(self, user_id):

        cursor = self.connection.cursor()

        sql = """
        INSERT INTO Progress
        (
            user_id,
            current_level,
            lessons_completed,
            quiz_completed,
            question_solved,
            accuracy,
            study_time,
            current_streak,
            overall_progress,
            last_login
        )
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """

        values = (
            user_id,
            1,
            0,
            0,
            0,
            0,
            0,
            1,
            0
        )

        cursor.execute(sql, values)

        self.connection.commit()
        cursor.close()
        
    def get_progress(self, user_id):
        cursor = self.connection.cursor(dictionary=True)
        sql = """
            SELECT *
            FROM Progress
            WHERE user_id = %s
            """
            
        cursor.execute(sql, (user_id,))

        progress = cursor.fetchone()

        cursor.close()

        return progress    
    
    def update_quiz_progress(self, user_id, question_solved, accuracy):
        
        try:
            
            cursor = self.connection.cursor()
            sql = """
            
            UPDATE progress
            SET
            question_solved = %s,
            quiz_completed = quiz_completed + 1,
            accuracy = %s,
            overall_progress = %s,
            last_login = NOW()
            WHERE user_id = %s
            """
            values = (

                question_solved,
                accuracy,
                accuracy,
                user_id
                
                )
            
            cursor.execute(sql, values)
            self.connection.commit()
            cursor.close()
            print("Progress updated successfully")
            
        except Exception as e:
            print("Progress update error:", e)
        
        
        
    def update_level(self, user_id, level, overall_progress):
        
        cursor = self.connection.cursor()
        
        sql = """
        
        UPDATE progress
        SET current_level = %s,
            overall_progress = %s,
            last_login = NOW()
        WHERE user_id = %s
        """
        

        values = (
        level,
        overall_progress,
        user_id
    )
        
        cursor.execute(sql, values)

        self.connection.commit()
        cursor.close()
    
    
    def update_overall_progress(
        self,
        user_id,
        overall_progress
):

        cursor = self.connection.cursor()

        sql = """
        UPDATE Progress
        SET overall_progress = %s
        WHERE user_id = %s
        """

        cursor.execute(
        sql,
        (overall_progress, user_id)
    )

        self.connection.commit()

        cursor.close()    
            
        
    def update_after_quiz(
    self,
    user_id,
    level,
    question_solved,
    accuracy,
    study_time
):
        

       cursor = self.connection.cursor()

       overall_progress = (level / 6) * 100

       cursor.execute("""
        UPDATE progress
        SET
            current_level = %s,
            quiz_completed = quiz_completed + 1,
            question_solved = question_solved + %s,
            accuracy = %s,
            study_time = study_time + %s,
            overall_progress = %s,
            last_login = NOW()
        WHERE user_id = %s
        """, (
        level,
        question_solved,
        accuracy,
        study_time,
        overall_progress,
        user_id
    ))
       

       self.connection.commit()
       cursor.close()    