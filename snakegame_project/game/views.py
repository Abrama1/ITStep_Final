from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from .models import GameHistory, Achievement
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('game')
        else:
            messages.error(request, form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'game/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('game')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'game/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


def game(request):
    return render(request, 'game/game.html')


@login_required
def history(request):
    game_history = GameHistory.objects.filter(user=request.user).order_by('-played_at')
    return render(request, 'game/history.html', {'game_history': game_history})


@csrf_exempt
@login_required
def save_game_result(request):
    if request.method == 'POST':
        score = int(request.POST.get('score'))
        GameHistory.objects.create(user=request.user, score=score)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})


def leaderboard(request):
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)

    daily_scores = GameHistory.objects.filter(played_at__date=today).order_by('-score')[:10]
    weekly_scores = GameHistory.objects.filter(played_at__date__gte=week_ago).order_by('-score')[:10]
    all_time_scores = GameHistory.objects.order_by('-score')[:10]

    context = {
        'daily_scores': daily_scores,
        'weekly_scores': weekly_scores,
        'all_time_scores': all_time_scores
    }
    return render(request, 'game/leaderboard.html', context)


@login_required
def profile(request):
    user = request.user
    best_score = GameHistory.objects.filter(user=user).order_by('-score').first()

    # Retrieve achievements based on user's best score
    if best_score:
        achievements_unlocked = Achievement.objects.filter(threshold_score__lte=best_score.score)
    else:
        achievements_unlocked = Achievement.objects.none()  # Return an empty queryset if no best_score
    return render(request, 'game/profile.html', {
        'username': user.username,
        'date_joined': user.date_joined,
        'best_score': best_score.score if best_score else None,
        'achievements': achievements_unlocked
    })
