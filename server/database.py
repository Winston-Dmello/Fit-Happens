from mysql import connector

class DB:
    def __init__(self):
        # Establish a connection to the MySQL server
        #nanda
        #newpassword
        connection_config = {
            "host": "localhost",
            "user": "nanda",
            "password": "newpassword"
        }
        self.db = connector.connect(**connection_config)
        self.cursor = self.db.cursor()

        # Create the FitHappens database if it doesn't exist
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS FitHappens")
        self.cursor.execute("USE FitHappens")

        # Create the Scoreboard table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Scoreboard (
                username VARCHAR(50),
                score INT
            )
        """)

        # Create the Users table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                username VARCHAR(50) PRIMARY KEY,
                password VARCHAR(50)
            )
        """)

        # Create the Runs table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Runs (
                runid INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50),
                date DATE,
                score INT,
                death_by VARCHAR(50),
                jump_count INT,
                duck_count INT,
                dodge_count INT,
                FOREIGN KEY (username) REFERENCES Users(username)
            )
        """)

        # Commit the changes to the database
        self.db.commit()

    def insert_score(self, username, score):
        self.cursor.execute("Use FitHappens")
        self.cursor.execute("INSERT INTO Scoreboard VALUES (%s, %s)", (username, score))
        self.db.commit()
    
    def get_scoreboard(self):
        self.cursor.execute("Use FitHappens")
        self.cursor.execute("SELECT * FROM Scoreboard ORDER BY Score DESC LIMIT 10")
        rows = self.cursor.fetchall()
        usrs = []
        scrs = []

        for (i,j) in rows:
            usrs.append(i)
            scrs.append(j)

        return {"Usernames": usrs, "Scores": scrs}
    
    def user_exists(self, username):
        self.cursor.execute("Use FitHappens")
        self.cursor.execute("SELECT * FROM Users WHERE Username = %s", (username,))
        if self.cursor.fetchone():
            return True
        else:
            return False
        
    def create_user(self, username, password):
        self.cursor.execute("Use FitHappens")
        self.cursor.execute("INSERT INTO Users VALUES (%s, %s)", (username, password))
        self.db.commit()

    def login_user(self, username, password):
        self.cursor.execute("Use FitHappens")
        self.cursor.execute("SELECT * FROM Users WHERE Username = %s AND Password = %s", (username, password))
        if self.cursor.fetchone():
            return True
        else:
            return False
        
    def get_runs_by_username(self, username):
        self.cursor.execute("Use FitHappens")
        self.cursor.execute("SELECT * FROM Runs WHERE Username = %s ORDER BY RunID DESC LIMIT 11", (username,))
        return self.cursor.fetchall()
    
    def insert_run(self, runs):
        self.cursor.execute("Use FitHappens")
        self.cursor.execute("INSERT INTO Runs (username, date, score, death_by, jump_count, duck_count, dodge_count) VALUES (%s, CURDATE(), %s, %s, %s, %s, %s)", 
                                (runs["Username"],  runs["Score"], "Obesity", runs["JumpingJack"], runs["Squat"], runs["Dodge"]))
        self.db.commit()