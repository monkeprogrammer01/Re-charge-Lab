from django.http import JsonResponse
from django.shortcuts import render


def telegram_connect(request):
    if request.method == "POST":
        token = request.user.token
        telegram_url = f"https://t.me/TechnoPulse1Bot?start={token}"
        return JsonResponse({
            'status': 'success',
            'telegram_url': telegram_url,
            'message': "Use this link to connect telegram."
        })
    return render(request, 'telegram_bot/telegram_connect.html')