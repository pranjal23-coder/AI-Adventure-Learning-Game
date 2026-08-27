class MissionModel:

    def __init__(self, connection):
        self.connection = connection


    def get_mission_progress(self, user_id, level):

        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                mission_number,
                completed
            FROM mission_progress
            WHERE user_id = %s
            AND levels = %s
            ORDER BY mission_number
        """, (user_id, level))

        missions = cursor.fetchall()

        cursor.close()

        return missions


    def complete_mission(
        self,
        user_id,
        level,
        mission_number
    ):

        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO mission_progress
            (
                user_id,
                levels,
                mission_number,
                completed,
                completed_at
            )
            VALUES
            (
                %s,
                %s,
                %s,
                TRUE,
                NOW()
            )

            ON DUPLICATE KEY UPDATE
                completed = TRUE,
                completed_at = NOW()
        """, (
            user_id,
            level,
            mission_number
        ))

        self.connection.commit()

        cursor.close()