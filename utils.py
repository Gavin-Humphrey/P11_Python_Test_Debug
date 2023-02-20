import json
import datetime




def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        comp_date_format = "%Y-%m-%d %H:%M:%S"
        listOfCompetitions = json.load(comps)['competitions']
        for competition in listOfCompetitions:
            competition['date'] = datetime.datetime.strptime(competition['date'], comp_date_format)
            if competition['date'] < datetime.datetime.now():
                competition['past_competition'] = True 
            else:
                competition['past_competition'] = False
        return listOfCompetitions