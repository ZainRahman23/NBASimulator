from flask import *
from database import init_db, db_session
from models import *
import random

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "Change Me"



# TODO: Fill in methods and routes
@app.route("/")
def home():
    if "username" in session:
        user = db_session.query(User).filter_by(username=session["username"]).first()
        teams = db_session.query(Result).filter_by(user_id = user.id).order_by(Result.points.desc()).all()
        rank = 0
        for team in teams:
            rank += 1

            if team.team_id == user.team_id:
                current_team = team
                break
        
        if rank == 1:
            rankStr = "1st"
        elif rank == 2:
            rankStr = "2nd"
        elif rank == 3:
            rankStr = "3rd"
        else:
            rankStr = str(rank) + "th"

        playable_teams = db_session.query(Result).filter_by(user_id = user.id).filter_by(played = 0).order_by(Result.points.desc()).all()
        if len(playable_teams) > 0:
            playing_team = random.choice(playable_teams)
        else:
            return render_template("seasonOver.html", team_name = current_team.team.team_name, wins = str(current_team.wins), losses = str(current_team.losses), rank = rankStr)

        return render_template("index.html", team_name = current_team.team.team_name, playing_team = playing_team, wins = str(current_team.wins), losses = str(current_team.losses), rank = rankStr)
    else:
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]

        users = db_session.query(User).filter_by(username = username).filter_by(password = password)
        if users.count() != 0:
            session["username"] = username
            return redirect(url_for("home"))
        else:
            flash("Incorrect Username or Password", "info")
            return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form["username"]
        password = request.form["password"]

        if db_session.query(User).filter_by(username = username).count() != 0:
                flash("Username is already taken", "info")
                return render_template("signup.html")
        registered_user = User(username=username, password = password)
        db_session.add(registered_user)
        db_session.commit()
        session["username"] = username
        return redirect(url_for("selectTeam"))

@app.route("/selectTeam", methods=["GET"])
def selectTeam():
    if "username" in session:
        args=request.args.to_dict()
        if "team" in args:
            user = db_session.query(User).filter_by(username=session["username"]).first()
            current_team = db_session.query(Team).filter_by(team_name= args["team"]).first()
            user.team = current_team
            db_session.commit()
            teams = db_session.query(Team).all()
            for team in teams:
                played = 0
                if(team.id == current_team.id):
                    played = 1
                result = Result(team.id, user.id, 0, 0, played)
                db_session.add(result)
                db_session.commit()
            return redirect(url_for("home"))
        return render_template("selectTeam.html")
    else:
        return redirect(url_for("login"))

@app.route("/result")
def result():
    if "username" in session:
        args=request.args.to_dict()
        if "team" not in args:
            return redirect(url_for("home"))
        user = db_session.query(User).filter_by(username=session["username"]).first()
        teams = db_session.query(Result).filter_by(user_id = user.id).order_by(Result.points.desc()).all()
        rank = 0
        for team in teams:
            rank += 1

            if team.team_id == user.team_id:
                current_team = team
                break
        
        if rank == 1:
            rankStr = "1st"
        elif rank == 2:
            rankStr = "2nd"
        elif rank == 3:
            rankStr = "3rd"
        else:
            rankStr = str(rank) + "th"
        playing_team = db_session.query(Result).filter_by(team_id = args["team"]).filter_by(user_id=user.id).first()
        win_chance = current_team.team.rating / (current_team.team.rating+playing_team.team.rating)
        result = ""
        if random.random() <= win_chance:
            result = "Won!"
            current_team.wins += 1
            current_team.points += 1
            playing_team.losses += 1
            playing_team.points -= 1
            playing_team.played = 1
        else:
            result = "Loss!"
            current_team.losses += 1
            current_team.points -= 1
            playing_team.wins += 1
            playing_team.points += 1
            playing_team.played = 1
        
        db_session.commit()

        other_teams = []
        for team in teams:
            if team.team_id != current_team.team_id and team.team_id != playing_team.team_id:
                other_teams.append(team)
        random.shuffle(other_teams)
        while len(other_teams) > 1:  
            first_team = other_teams.pop()
            second_team = other_teams.pop()

            win_chance = first_team.team.rating / (first_team.team.rating+second_team.team.rating)
            if random.random() <= win_chance:
                first_team.wins += 1
                first_team.points += 1
                second_team.losses += 1
                second_team.points -= 1
            else:
                first_team.losses += 1
                first_team.points -= 1
                second_team.wins += 1
                second_team.points += 1
            
            db_session.commit()



        return render_template("result.html", result = result, playing_team = playing_team,  team_name = current_team.team.team_name, wins = str(current_team.wins), losses = str(current_team.losses), rank = rankStr)
    else:
        return redirect(url_for("login"))

@app.route("/leaderboard")
def leaderboard():
    if "username" in session:
        user = db_session.query(User).filter_by(username=session["username"]).first()
        teams = db_session.query(Result).filter_by(user_id = user.id).order_by(Result.points.desc()).all()
        rank = 0
        for team in teams:
            rank += 1

            if team.team_id == user.team_id:
                current_team = team
                break
        
        if rank == 1:
            rankStr = "1st"
        elif rank == 2:
            rankStr = "2nd"
        elif rank == 3:
            rankStr = "3rd"
        else:
            rankStr = str(rank) + "th"

        return render_template("leaderboard.html", teams = teams, team_name = current_team.team.team_name, wins = str(current_team.wins), losses = str(current_team.losses), rank = rankStr)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("username")
    return redirect(url_for("login"))


with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
