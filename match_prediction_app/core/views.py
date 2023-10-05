from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.http import require_POST
from render_block import render_block_to_string

from match_prediction_app.core.models import Fixture
from match_prediction_app.core.models import Prediction


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """
    Render and return the index.html template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    fixtures = Fixture.objects.all()

    predictions = [f.predictions.filter(user=request.user).first() for f in fixtures]

    context = {
        "fixtures_and_predictions": zip(fixtures, predictions, strict=True),
    }
    return render(request, "home.html", context)


@login_required
@require_POST
def submit_prediction(request: HttpRequest, fixture_pk: int) -> HttpResponse:
    """
    Render and return the submit_prediction.html template.

    Args:
        request (HttpRequest): The HTTP request object.
        fixture_pk (int): The fixture PK.

    Returns:
        HttpResponse: The HTTP response object.
    """
    fixture = get_object_or_404(Fixture, pk=fixture_pk)

    home_goals = int(request.POST.get("home_goals"))
    away_goals = int(request.POST.get("away_goals"))

    prediction = Prediction.objects.filter(user=request.user, fixture=fixture).first()

    if prediction:
        prediction.home_goals = home_goals
        prediction.away_goals = away_goals
        prediction.save()
    else:
        prediction = Prediction.objects.create(
            user=request.user,
            fixture=fixture,
            home_goals=home_goals,
            away_goals=away_goals,
        )

    context = {"prediction": prediction, "fixture": fixture}

    html = render_block_to_string("home.html", "fixture-container", context)

    return HttpResponse(html)


@login_required
@require_POST
def delete_prediction(request: HttpRequest, prediction_pk: int) -> HttpResponse:
    """
    Render and return the delete_prediction.html template.

    Args:
        request (HttpRequest): The HTTP request object.
        prediction_pk (int): The prediction PK.

    Returns:
        HttpResponse: The HTTP response object.
    """
    prediction = get_object_or_404(Prediction, pk=prediction_pk)
    fixture = prediction.fixture
    prediction.delete()

    context = {"prediction": None, "fixture": fixture}

    html = render_block_to_string("home.html", "fixture-container", context)

    return HttpResponse(html)
