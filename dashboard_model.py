from db import connection

class DashboardModel:
    def __init__(self, connection):
            self.connection = connection

    def get_dashboard_data(self, user_id):

        cursor = connection.cursor(dictionary=True)

        sql = """
        SELECT
            COALESCE(SUM(score),0) AS total_score,
            COALESCE(SUM(total_questions),0) AS total_questions,
            COALESCE(MAX(level),1) AS current_level
        FROM quiz_results
        WHERE user_id=%s
        """

        cursor.execute(sql, (user_id,))
        quiz = cursor.fetchone()

        accuracy = 0

        if quiz["total_questions"] > 0:
            accuracy = round(
                (quiz["total_score"] /
                 quiz["total_questions"]) * 100
            )

        data = {
            "accuracy": accuracy,
            "questions_solved": quiz["total_questions"],
            "current_level": quiz["current_level"],
            "study_time": "0 min",
            "streak": 0,
            "rank": "Beginner",
            "overall_progress": quiz["current_level"] * 16
        }

        cursor.close()

        return data