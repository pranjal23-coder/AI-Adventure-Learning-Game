from db import connection

class QuizModel:
    def __init__(self, connection):
            self.connection= connection
            
    def create_quiz(self, topic, levels, question, option_a,option_b,option_c,option_d,correct_answer,explanation,xp_reward):
        cursor = self.connection.cursor(dictionary=True)
        query = """
        INSERT INTO Quiz (topic, levels, question, option_a,option_b,
                                       option_c,
                                       option_d,
                                       correct_answer,
                                       explanation,
                                       xp_reward)
        VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s)
        """
        
        values=(topic,levels, question, option_a,option_b,option_c,option_d,correct_answer,explanation,xp_reward)
        cursor.execute(query, values)
                            
        connection.commit()
        cursor.close()




    def get_questions_by_level(self, level):

        cursor = self.connection.cursor(dictionary=True)

        sql = """
            SELECT *
            FROM Quiz
            WHERE levels = %s
            ORDER BY id
        """

        cursor.execute(sql, (level,))

        questions = cursor.fetchall()

        cursor.close()

        return questions    