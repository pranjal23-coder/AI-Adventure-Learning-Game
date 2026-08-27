import os
from flask import Flask,render_template,request,redirect,url_for,session,flash
from werkzeug.utils import secure_filename
from db import connection
from models.user_model import UsersModel
from models.progress_model import ProgressModel
from models.lesson_model import LessonModel
from models.quiz_model import QuizModel
from models.quiz_result_model import QuizResultModel
from models.achievement_model import AchievementModel
from models.leaderboard_model import LeaderboardModel
from models.ai_recommendation_model import AIRecommendationModel
from models.dashboard_model import DashboardModel
from models.mission_model import MissionModel

import pandas as pd
import joblib


user_model=UsersModel(connection)
progress_model=ProgressModel(connection)
lesson_model=LessonModel(connection)
quiz_model=QuizModel(connection)
quiz_result_model=QuizResultModel(connection)
achievement_model=AchievementModel(connection)
leaderboard_model=LeaderboardModel(connection)
ai_recommendation_model=AIRecommendationModel(connection)
dashboard_model= DashboardModel(connection)
mission_model=MissionModel(connection)


app=Flask(__name__)
app.secret_key="your_mysql"
UPLOAD_FOLDER = os.path.join(
    app.static_folder,
    "uploads"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg"
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )



recommendation_model=joblib.load(
    "ml/recommendation_model.pkl"
)

recommendation_encoder=joblib.load(
    "ml/recommendation_encoder.pkl"
)

# ==========================================
# AI RECOMMENDATION FUNCTION
# ==========================================

def get_recommendation(progress):

    data = pd.DataFrame([{
        "accuracy": float(progress.get("accuracy", 0)),
        "current_level": int(progress.get("current_level", 1)),
        "lessons_completed": int(progress.get("lessons_completed", 0)),
        "quiz_completed": int(progress.get("quiz_completed", 0)),
        "study_time": int(progress.get("study_time", 0)),
        "current_streak": int(progress.get("current_streak", 0)),
        "overall_progress": float(progress.get("overall_progress", 0))
    }])

    prediction = recommendation_model.predict(data)

    recommendation = recommendation_encoder.inverse_transform(
        prediction
    )

    return recommendation[0]




@app.route("/")
def splash():
   return render_template("splash.html")

@app.route("/welcome")
def welcome():  
    return render_template("welcome.html")
    
"""   
  
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    
    recommendation = "Keep practicing to improve your coding skills."

    # Get user progress
    progress = progress_model.get_progress(user_id)
    print("DASHBOARD USER ID:", user_id)
    print("DASHBOARD PROGRESS:", progress)
    print("DASHBOARD STUDY TIME:", progress.get("study_time") if progress else "NO PROGRESS")
    

    # Default values
    overall_progress = 0
    accuracy = 0
    questions_solved = 0
    current_level = 1
    current_streak = 0
    study_time = 0

    if progress:

        overall_progress = progress.get("overall_progress") or 0
        accuracy = progress.get("accuracy") or 0
        questions_solved = progress.get("question_solved") or 0
        current_level = progress.get("current_level") or 1
        current_streak = progress.get("current_streak") or 0
        study_time = progress.get("study_time") or 0

    # Convert numbers safely
    try:
        overall_progress = round(float(overall_progress), 2)
    except:
        overall_progress = 0

    try:
        accuracy = round(float(accuracy), 2)
    except:
        accuracy = 0
        
      

    return render_template(
        "dashboard.html",
        
    

        progress=progress,

        overall_progress=overall_progress,
        accuracy=accuracy,
        questions_solved=questions_solved,
        current_level=current_level,
        current_streak=current_streak,
        recommendation=recommendation,
        study_time=study_time
        
    )
    
""" 
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # Default recommendation
    recommendation = "Keep practicing to improve your coding skills."

    # Get user progress
    progress = progress_model.get_progress(user_id)
    progress = progress_model.get_progress(user_id)

    if progress is None:
     progress = {
        "current_level": 1,
        "lessons_completed": 0,
        "quiz_completed": 0,
        "question_solved": 0,
        "accuracy": 0,
        "study_time": 0,
        "current_streak": 0,
        "overall_progress": 0,
        "last_login": None
    }

    # Get latest AI recommendation
    ai_rec = ai_recommendation_model.get_latest_recommendation(user_id)

    if ai_rec:
        recommendation = ai_rec

    # Default values
    overall_progress = 0
    accuracy = 0
    questions_solved = 0
    current_level = 1
    current_streak = 0
    study_time = 0

    if progress:

        overall_progress = progress.get("overall_progress") or 0
        accuracy = progress.get("accuracy") or 0
        questions_solved = progress.get("question_solved") or 0
        current_level = progress.get("current_level") or 1
        current_streak = progress.get("current_streak") or 0
        study_time = progress.get("study_time") or 0

    try:
        overall_progress = round(float(overall_progress), 2)
    except:
        overall_progress = 0

    try:
        accuracy = round(float(accuracy), 2)
    except:
        accuracy = 0

    return render_template(
        "dashboard.html",

        progress=progress,

        overall_progress=overall_progress,
        accuracy=accuracy,
        questions_solved=questions_solved,
        current_level=current_level,
        current_streak=current_streak,
        study_time=study_time,
        recommendation=recommendation
    )
        
@app.route("/login",methods=["GET","POST"])

def login():

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        data=user_model.login_user(
            username,
            password
        )

        if data:

            session["user_id"]=data["user_id"]
            session["username"]= data["username"]
            return redirect (url_for("dashboard"))
        return "Invalid Login"

    return render_template("login.html")


@app.route("/register",methods=["GET","POST"])

def register():

    if request.method=="POST":

        fullname=request.form["fullname"]
        username=request.form["username"]
        email=request.form["email"]
        password=request.form["password"]

        user_id=user_model.create_user(
            fullname,
            username,
            email,
            password
        )

        progress_model.create_progress(user_id)
        
        leaderboard_model.create_leaderboard(
            user_id=user_id,
            total_score=0,
            rank_position=0
            
        )

        return redirect("/login")

    return render_template("register.html")

    
@app.route("/levels")
def levels():
    return render_template("levels.html")


@app.route('/lesson/<int:level>/<int:mission_number>')
def lesson(level, mission_number):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    lesson = lesson_model.get_lesson_by_level_and_mission(
        level,
        mission_number
    )

    if not lesson:
        return "Lesson not found", 404

    return render_template(
        'lesson.html',
        lesson=lesson,
        level=level,
        mission_number=mission_number
    )
    

@app.route("/quiz/<int:level>")
def quiz(level):

    questions=quiz_model.get_questions_by_level(level)
    print("quiz level:", level)
    print("no. of que:", len(questions))
    print("quiz que:", questions)

    return render_template(
        "quiz.html",
        questions=questions,
        level=level,
       
    )


@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():

    # --------------------------------
    # 1. CHECK LOGIN
    # --------------------------------
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    recommendation="Keep practicing to improve your coding skills. "

    # --------------------------------
    # 2. GET LEVEL
    # --------------------------------
    level = int(request.form.get("level", 1))

    # --------------------------------
    # 3. GET QUESTIONS
    # --------------------------------
    questions = quiz_model.get_questions_by_level(level)

    if not questions:
        return "No questions found for this level."

    # --------------------------------
    # 4. CALCULATE RESULT
    # --------------------------------
    correct = 0
    total_questions = len(questions)

    # Get total quiz time from hidden field
    time_taken = int(request.form.get("time_taken", 0))

    print("--------------------------------")
    print("QUIZ SUBMITTED")
    print("User ID:", user_id)
    print("Level:", level)
    print("Total Questions:", total_questions)
    print("Time Taken:", time_taken)
    print("--------------------------------")

    # --------------------------------
    # 5. SAVE EACH QUESTION RESULT
    # --------------------------------
    for question in questions:

        question_id = question["id"]

        # Selected answer from form
        selected_answer = request.form.get(
            f"question_{question_id}",""
        )

        # Correct answer from database
        correct_answer = question["correct_answer"]

        # Remove spaces and convert to uppercase
        selected_clean = (
            selected_answer.strip().upper()
            if selected_answer
            else ""
        )

        correct_clean = (
            str(correct_answer).strip().upper()
        )

        # Check answer
        is_correct = (
            selected_clean != ""
            and selected_clean == correct_clean
        )

        # Calculate score
        if is_correct:
            correct += 1
            score = 10
        else:
            score = 0

        print(
            "Question:", question_id,
            "| Selected:", selected_clean,
            "| Correct:", correct_clean,
            "| Is Correct:", is_correct,
            "| Score:", score
        )

        # --------------------------------
        # SAVE RESULT
        # --------------------------------
        try:

            quiz_result_model.save_result(
                user_id=user_id,
                quiz_question_id=question_id,
                selected_question=selected_clean,
                is_correct=1 if is_correct else 0,
                score=score,
                time_taken=time_taken
            )

        except Exception as e:

            print(
                "Quiz result save error:",
                e
            )

    # --------------------------------
    # 6. ACCURACY
    # --------------------------------
    if total_questions > 0:

        accuracy = round(
            (correct / total_questions) * 100,
            2
        )

    else:

        accuracy = 0

    # --------------------------------
    # 7. XP
    # --------------------------------
    xp = correct * 10

    print("--------------------------------")
    print("Correct:", correct)
    print("Total:", total_questions)
    print("Accuracy:", accuracy)
    print("XP:", xp)
    print("--------------------------------")

    # --------------------------------
    # 8. UPDATE LEADERBOARD
    # --------------------------------
    try:
        if not connection.is_connected():
            connection.reconnect(attempts=3, delay=1)

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE leaderboard
            SET total_score = total_score + %s
            WHERE user_id = %s
        """, (xp, user_id))

        connection.commit()
        cursor.close()

        print("Leaderboard updated successfully")

    except Exception as e:

        print("Leaderboard update error:",e)

    # --------------------------------
    # 9. UPDATE ACHIEVEMENT
    # --------------------------------
    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT total_xp
            FROM achievement
            WHERE user_id = %s
        """, (user_id,))

        achievement = cursor.fetchone()

        if achievement is None:

            new_total_xp = xp

        else:

            new_total_xp = achievement[0] + xp

        # Decide badge
        if new_total_xp >= 1000:

            badge_value = "Code Master"
            star_value = 5
            title_value = "Code Master"

        elif new_total_xp >= 500:

            badge_value = "Coding Hero"
            star_value = 3
            title_value = "Coding Hero"

        elif new_total_xp >= 100:

            badge_value = "Code Explorer"
            star_value = 1
            title_value = "Code Explorer"

        else:

            badge_value = "Beginner"
            star_value = 0
            title_value = "Beginner"

        # Insert new achievement
        if achievement is None:

            cursor.execute("""
                INSERT INTO achievement
                (
                    user_id,
                    badges,
                    stars,
                    certificates,
                    total_xp,
                    unlocked_title
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                user_id,
                badge_value,
                star_value,
                0,
                new_total_xp,
                title_value
            ))

        # Update existing achievement
        else:

            cursor.execute("""
                UPDATE achievement
                SET
                    badges = %s,
                    stars = %s,
                    total_xp = %s,
                    unlocked_title = %s
                WHERE user_id = %s
            """, (
                badge_value,
                star_value,
                new_total_xp,
                title_value,
                user_id
            ))

        connection.commit()
        cursor.close()

        print("Achievement updated successfully")

    except Exception as e:

        print(
            "Achievement update error:",
            e
        )

    # --------------------------------
    # 10. UPDATE QUIZ PROGRESS
    # --------------------------------
    try:

        progress_model.update_quiz_progress(
            user_id,
            total_questions,
            accuracy
        )

        print(
            "Quiz progress updated successfully"
        )

    except Exception as e:

        print(
            "Quiz progress update error:",
            e
        )

    # --------------------------------
    # 11. UPDATE GENERAL PROGRESS
    # --------------------------------
    try:

        progress_model.update_after_quiz(
            user_id=user_id,
            level=level,
            question_solved=total_questions,
            accuracy=accuracy,
            study_time=time_taken
        )

        print(
            "General progress updated successfully"
        )

    except Exception as e:

        print(
            "General progress update error:",
            e
        )
        
  
        # UPDATE CURRENT STREAK
        
    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
        SELECT current_streak, last_login
        FROM progress
        WHERE user_id = %s
        """, (user_id,))

        progress_data = cursor.fetchone()

        from datetime import datetime, timedelta

        today = datetime.now().date()
        

        if progress_data and progress_data["last_login"]:

           last_login = progress_data["last_login"].date()
           

           if last_login == today:
            # Already active today
            new_streak = progress_data["current_streak"]

           elif last_login == today - timedelta(days=1):
            # Continued from yesterday
            new_streak = progress_data["current_streak"] + 1

           else:
            # Streak broken
            new_streak = 1
        else:
              
        
           
         new_streak = 1

         cursor.execute("""
        UPDATE progress
        SET
            current_streak = %s,
            last_login = NOW()
        WHERE user_id = %s
         """, (new_streak, user_id))

        connection.commit()
        cursor.close()

        print("🔥 Current Streak:", new_streak)

    except Exception as e:
       print("Streak update error:", e)

    # --------------------------------
    # 12. LEVEL / OVERALL PROGRESS
    # --------------------------------
    next_level = level

    if accuracy >= 70:

        next_level = level + 1

        if next_level > 6:
            next_level = 6

    overall_progress = round(
        (next_level / 6) * 100,
        2
    )
     # --------------------------------
    # 13. UPDATE LEVEL
    # --------------------------------
    try:

        progress_model.update_level(
            user_id,
            next_level,
            overall_progress
        )

        print(
            "Level and overall progress updated successfully"
        )

    except Exception as e:

        print(
            "Level update error:",
            e
        )
        
   
        
            # AI RECOMMENDATION
        recommendation=ai_recommendation_model.get_latest_recommendation(user_id)
        if not recommendation:
            recommendation="keep practicing to improve your coding skills."
   

        progress=progress_model.get_progress(user_id)
    
        progress["accuracy"] = accuracy
        progress["current_level"] = next_level

        recommendation = get_recommendation(progress)
    
        print("================================")
        print("AI RECOMMENDATION")
        print("User ID:", user_id)
        print("Recommendation:", recommendation)
        print("================================")

        ai_recommendation_model.save_recommendation(
               user_id,
              str(recommendation)
            )

        print("AI recommendation saved successfully")

    except Exception as e:

        print("AI recommendation error:", e)
       # --------------------------------
       # 14. RESULT PAGE
        # --------------------------------
    return render_template(
        "result.html",
        correct=correct,
        total_questions=total_questions,
        accuracy=accuracy,
        xp=xp,
        level=level,
        next_level=next_level,
        recommendation=recommendation
    )  
      
@app.route("/quiz_result")
def quiz_result():
    return render_template("quiz_result.html")

@app.route("/leaderboard")
def leaderboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            l.user_id,
            u.username,
            u.profile_image,
            l.total_score,
            l.rank_position
            FROM leaderboard l
            JOIN users u
            ON l.user_id = u.user_id
            ORDER BY l.total_score DESC
            """)

    leaderboard_data = cursor.fetchall()
    cursor.close()

    # Calculate ranks
    for index, row in enumerate(leaderboard_data, start=1):
        row["rank_position"] = index
    

    return render_template(
        "leaderboard.html",
        leaderboard=leaderboard_data
    )
    
    
@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    user = user_model.get_user(user_id)

    if not user:
        return "User not found."

    progress = progress_model.get_progress(user_id)

    return render_template(
        "profile.html",
        user=user,
        progress=progress
    )

@app.route("/settings", methods=["GET", "POST"])
def settings():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        sound = request.form.get("sound") == "on"
        music = request.form.get("music") == "on"
        notifications = request.form.get("notifications") == "on"
        language = request.form.get("language", "English")

        print("--------------------------------")
        print("SETTINGS SAVED")
        print("User ID:", session["user_id"])
        print("Sound:", sound)
        print("Music:", music)
        print("Notifications:", notifications)
        print("Language:", language)
        print("--------------------------------")

        return render_template(
            "settings.html",
            saved=True
        )

    return render_template(
        "settings.html",
        saved=False
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")



@app.route("/recommendation")
def recommendation_page():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    data = ai_recommendation_model.get_recommendation(user_id)

    if data:
        recommendation_text = data["recommendation"]
    else:
        recommendation_text = "Keep practicing to improve your coding skills."

    return render_template(
        "recommendation.html",
        recommendation=recommendation_text
    )


@app.route("/missions/<int:level>")
def missions(level):

    if "user_id" not in session:
        return redirect(url_for("login"))

    mission_list = lesson_model.get_lessons_by_level(level)

    return render_template(
        "missions.html",
        level=level,
        missions=mission_list
    )
    
@app.route('/complete_mission/<int:level>/<int:mission_number>',
           methods=['POST'])
def complete_mission(level, mission_number):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    try:

        # --------------------------------
        # 1. MARK MISSION AS COMPLETED
        # --------------------------------

        missions.complete_mission(
            user_id,
            level,
            mission_number
        )

        print("Mission completed successfully")
        print("User:", user_id)
        print("Level:", level)
        print("Mission:", mission_number)


        # --------------------------------
        # 2. GET CURRENT PROGRESS
        # --------------------------------

        progress = progress_model.get_progress(user_id)

        current_level = 1

        if progress:
            current_level = progress.get(
                'current_level',
                1
            ) or 1


        # --------------------------------
        # 3. UNLOCK NEXT LEVEL
        # --------------------------------

        # Assuming each level has 3 missions
        if mission_number == 3:

            next_level = level + 1

            if next_level > 6:
                next_level = 6

            if next_level > current_level:

                progress_model.update_level(
                    user_id,
                    next_level
                )

                print(
                    "Next level unlocked:",
                    next_level
                )


        # --------------------------------
        # 4. RETURN TO MISSIONS
        # --------------------------------

        return redirect(
            url_for(
                'missions',
                level=level
            )
        )

    except Exception as e:

        print(
            "Complete mission error:",
            e
        )

        return f"Error completing mission: {e}"
    
@app.route("/achievement")
def achievement():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    achievement = achievement_model.get_achievement(user_id)

    if achievement is None:
        achievement = {
            "badges": "beginner",
            "stars": 0,
            "certificates": 0,
            "total_xp": 0,
            "unlocked_title": "Beginner"
        }

    # Get progress
    progress_model_data = progress_model.get_progress(user_id)

    # Get leaderboard rank
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT rank_position
        FROM leaderboard
        WHERE user_id = %s
    """, (user_id,))

    rank_data = cursor.fetchone()

    cursor.close()

    if rank_data:
        global_rank = rank_data["rank_position"]
    else:
        global_rank = "Not Ranked"

    return render_template(
        "achievement.html",
        achievement=achievement,
        progress=progress_model_data,
        global_rank=global_rank
    )
    
@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    from db import connection

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    username = request.form.get('username')
    email = request.form.get('email')

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET 
            username = %s,
            email = %s
        WHERE user_id = %s
    """, ( username, email, user_id))

    connection.commit()
    cursor.close()
    return redirect(url_for('profile'))
    
@app.route('/change_password', methods=['POST'])
def change_password():

    from db import connection

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    current_password = request.form.get('current_password', '').strip()
    new_password = request.form.get('new_password', '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()

    # Check new passwords
    if new_password != confirm_password:
        return "New passwords do not match."

    if not new_password:
        return "New password cannot be empty."

    # IMPORTANT:
    # Your db.py connection is already a CMySQLConnection.
    # So use connection.cursor(), NOT connection.connection.cursor()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT password
        FROM users
        WHERE user_id = %s
    """, (user_id,))

    user = cursor.fetchone()

    if not user:
        cursor.close()
        return "User not found."

    stored_password = str(user[0]).strip()

    print("Entered password:", repr(current_password))
    print("Database password:", repr(stored_password))

    # Compare current password
    if current_password != stored_password:

        cursor.close()

        return "Current password is incorrect."

    # Update password
    cursor.execute("""
        UPDATE users
        SET password = %s
        WHERE user_id = %s
    """, (new_password, user_id))

    connection.commit()

    cursor.close()

    return redirect(url_for('profile'))

@app.route("/upload_profile_image", methods=["POST"])
def upload_profile_image():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # Check whether image was selected
    if "profile_image" not in request.files:
        flash("No image selected.", "error")
        return redirect(url_for("profile"))

    file = request.files["profile_image"]

    if file.filename == "":
        flash("Please select an image.", "error")
        return redirect(url_for("profile"))

    # Check file type
    if not allowed_file(file.filename):
        flash("Only JPG, JPEG and PNG images are allowed.", "error")
        return redirect(url_for("profile"))

    # Get extension
    extension = file.filename.rsplit(".", 1)[1].lower()

    # Unique filename for the logged-in user
    filename = f"user_{user_id}.{extension}"

    # Make sure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Complete file path
    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    # Save image
    file.save(filepath)

    # -----------------------------
    # SAVE IMAGE NAME IN DATABASE
    # -----------------------------

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET profile_image = %s
        WHERE user_id = %s
        """,
        (filename, user_id)
    )

    connection.commit()

    cursor.close()

    flash("Profile picture updated successfully!", "success")

    return redirect(url_for("profile"))

   
    
if __name__ =="__main__":
    app.run(debug=True)
     
