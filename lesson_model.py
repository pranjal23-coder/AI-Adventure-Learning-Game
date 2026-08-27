from db import connection


class LessonModel:

    def __init__(self, connection):
        self.connection = connection



    def add_lesson(
        self,
        levels,
        topic,
        lesson_title,
        lesson_content,
        difficulty,
        estimated_time,
        xp_reward,
        missions
    ):

        cursor = self.connection.cursor()

        query = """
        INSERT INTO Lessons
        (
            levels,
            topic,
            lesson_title,
            lesson_content,
            difficulty,
            estimated_time,
            xp_reward,
            missions
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            levels,
            topic,
            lesson_title,
            lesson_content,
            difficulty,
            estimated_time,
            xp_reward,
            missions
        )

        cursor.execute(query, values)

        self.connection.commit()

        cursor.close()



    def get_all_lessons(self):

        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM Lessons
            ORDER BY levels, missions
        """)

        lessons = cursor.fetchall()

        cursor.close()

        return lessons



    def get_lessons_by_level(self, level):

        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM Lessons
            WHERE levels = %s
            ORDER BY missions
        """, (level,))

        lessons = cursor.fetchall()

        cursor.close()

        return lessons



    def get_lesson(self, level, missions):

        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM Lessons
            WHERE levels = %s
            AND missions = %s
            LIMIT 1
        """, (level, missions))

        lesson = cursor.fetchone()

        cursor.close()

        return lesson


    def get_lesson_by_level_and_mission(
        self,
        level,
        mission_number
    ):

        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM Lessons
            WHERE levels = %s
            AND missions = %s
            LIMIT 1
        """, (level, mission_number))

        lesson = cursor.fetchone()

        cursor.close()

        return lesson