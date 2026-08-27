
class QuizResultModel:

    def __init__(self, connection):
        self.connection = connection


    def save_result(
        self,
        user_id,
        quiz_question_id,
        selected_question,
        is_correct,
        score,
        time_taken
    ):

        cursor = self.connection.cursor()

        sql = """
            INSERT INTO Quiz_Result
            (
                user_id,
                quiz_question_id,
                selected_question,
                is_correct,
                score,
                time_taken
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            user_id,
            quiz_question_id,
            selected_question,
            is_correct,
            score,
            time_taken
        )

        cursor.execute(sql, values)

        self.connection.commit()

        cursor.close()