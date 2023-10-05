from match_prediction_app.core.models import Fixture
from match_prediction_app.core.models import Team


# Register your models here.
def run():
    teams = [
        "Arsenal",
        "Chelsea",
        "Liverpool",
        "Manchester City",
        "Manchester United",
        "Tottenham Hotspur",
        "Real Madrid",
        "Barcelona",
        "Juventus",
        "Inter Milan",
        "Bayern Munich",
        "Ajax",
        "PSG",
        "Porto",
    ]

    # Create a team object for each team in the teams list
    for team in teams:
        Team.objects.create(name=team)

    teams = Team.objects.all()

    # for each pair of teams, create a fixture
    for team1, team2 in zip(teams[::2], teams[1::2], strict=True):
        Fixture.objects.get_or_create(home_team=team1, away_team=team2)
