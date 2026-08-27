AI Adventure Learning Game
1. Project Description

AI Adventure Learning Game is a web-based interactive coding learning platform designed to make programming education more engaging and enjoyable.

The platform combines learning lessons, coding quizzes, levels, progress tracking, achievements, leaderboard and AI-based recommendations in a single application.

2. Project Objective

The main objective of this project is to provide students with an interactive environment where they can learn programming concepts, test their knowledge through quizzes and track their learning progress.

3. Technologies Used

Frontend

* HTML
* CSS
* JavaScript

Backend

* Python
* Flask

Database

* MySQL

AI/ML

* AI-based learning recommendation system

Development Tools

* Visual Studio Code
* MySQL Workbench

4. Main Modules

* Login & Registration – Allows users to create an account and securely log in.
* Dashboard – Displays learning progress, XP, accuracy, questions solved, streak and other statistics.
* Levels – Provides different learning levels based on programming topics and difficulty.
* Lessons – Provides programming concepts and learning material.
* Coding Quiz – Allows users to answer programming-related questions and receive results.
* Progress Tracking – Tracks completed lessons, quizzes, accuracy and overall progress.
* Leaderboard – Displays user rankings based on performance.
* Achievements – Provides achievements based on learning activities and performance.
* Profile – Displays user information and learning statistics.
* Settings – Provides application/user settings.
* AI Recommendation – Suggests suitable learning content based on the user’s performance and progress.

5. Database Tables

The project uses MySQL for storing application data.

Main tables include:

* Users
* Lessons
* Quiz
* Quiz Results
* Progress
* Achievements
* Leaderboard
* AI Recommendations

The database SQL file is provided in the database folder.

6. Project Structure

AI_Adventure_Learning_Game/
│
├── app.py
├── requirements.txt
├── README.md
│
├── models/
│
├── templates/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── database/
│   └── ai_adventure_learning_game.sql
│
└── docs/
    ├── notes
    ├── Project_PPT.pptx
 

7. Requirements

Before running the project, make sure the following are installed:

* Python 3.x
* MySQL
* Visual Studio Code or another code editor
* Required Python packages listed in requirements.txt

8. Installation

Step 1: Open the Project

Open the project folder in Visual Studio Code.

Step 2: Install Required Packages

Open the terminal and run:

pip install -r requirements.txt

Step 3: Setup MySQL Database

1. Open MySQL Workbench.
2. Create the required database.
3. Import/run the SQL file provided in the database folder.
4. Configure the database connection in the project.

Step 4: Run the Application

Run:

python app.py

Step 5: Open the Website

Open the Flask URL displayed in the terminal, usually:

http://127.0.0.1:5000/

9. Project Outcome

The final application provides an interactive coding-learning experience where users can learn through lessons, practice through quizzes, monitor their progress and receive personalized learning recommendations.



Project: AI Adventure Learning Game
Type: Web-Based Learning Application
Backend: Python Flask
Database: MySQL

