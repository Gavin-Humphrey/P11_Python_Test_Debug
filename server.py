from flask import Flask,render_template,request,redirect,flash,url_for
import utils



MAX_PLACES = 12

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = utils.loadCompetitions()
clubs = utils.loadClubs()


def initialize_booking(comps, _clubs):
    places = []
    for comp in comps:
        for club in _clubs:
            places.append({'competition': comp['name'], 'booked': [0, club['name']]})
    return places


already_booked = initialize_booking(competitions, clubs)

def update_competition_booking(competition, club, places_required, already_booked):
    
    for i in already_booked:
        if i['competition'] == competition['name']:
            if i['booked'][0] + places_required <= MAX_PLACES:
                i['booked'][0] += places_required
                i['booked'][1] == club['name']
                break
            else:
                raise ValueError(f"Booking more than {MAX_PLACES} places in a competition is not allowed.")
    return already_booked

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions)
    except IndexError:
        if request.form['email'] == '':
            flash("Enter your email", 'error')
        else:
            flash("No corresponding email found!", 'error')
        return render_template('index.html'), 405 


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        if 'past_competition' in foundCompetition and foundCompetition['past_competition'] == True:
            flash(f"The {competition} competition is over and cannot be booked!")
            return render_template('welcome.html', club=foundClub, competitions=competitions), 400  
        return render_template('booking.html', club=foundClub,competition=foundCompetition, club_point=int(foundClub['points']), MAX_PLACES=MAX_PLACES)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)
    
@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    available_club_points = int(club['points'])  
    if places_required > available_club_points:
        flash("Isufficient points to book this amount of places.")
        return render_template('welcome.html', club=club, competitions=competitions), 400
    elif available_club_points < places_required :
        flash("Isufficient places available.")
        return render_template('welcome.html', club=club, competitions=competitions), 400
    
    #add max booking places
    try:        
        if places_required > MAX_PLACES:
            flash(f"You cannot book more than {MAX_PLACES} places in a single competition.")
            return render_template('welcome.html', club=club, competitions=competitions), 400
    
        #add point deduction
        else:
            update_competition_booking(competition, club, places_required, already_booked)
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-places_required
            club['points'] = available_club_points - places_required
            available_club_points = int(club['points']) - places_required
            flash('Great-booking complete!')
            return render_template('welcome.html', club=club, competitions=competitions)

    except ValueError as e:
        flash(str(e))
        return render_template('welcome.html', club=club, competitions=competitions)
   
# TODO: Add route for points display
@app.route("/display_board")
def display_board():
    return render_template("display_board.html", clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
