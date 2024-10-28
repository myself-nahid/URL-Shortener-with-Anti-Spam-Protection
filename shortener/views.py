# import necessary libraries
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from .models import ShortURL, BlockedIP, RequestLog
from .forms import URLForm
from datetime import timedelta
import random
import string

def generate_key():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def shorten_url(request):
    form = URLForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        original_url = form.cleaned_data['original_url']
        max_requests = form.cleaned_data['max_requests']
        block_duration = form.cleaned_data['block_duration']
        ip_address = get_client_ip(request)

        blocked_ip = BlockedIP.objects.filter(ip_address=ip_address).first()
        if blocked_ip and blocked_ip.is_blocked():
            return HttpResponse("You are temporarily blocked due to excessive requests.", status=403)

        RequestLog.objects.create(ip_address=ip_address)

        time_threshold = timezone.now() - timedelta(minutes=1)
        recent_requests_count = RequestLog.objects.filter(
            ip_address=ip_address,
            accessed_at__gte=time_threshold
        ).count()

        if recent_requests_count >= max_requests:
            blocked_until = timezone.now() + timedelta(minutes=block_duration)
            BlockedIP.objects.update_or_create(ip_address=ip_address, defaults={'blocked_until': blocked_until})
            return HttpResponse("You are temporarily blocked due to excessive requests.", status=403)

        short_url, created = ShortURL.objects.get_or_create(original_url=original_url)
        if created:
            short_url.short_key = generate_key()
            short_url.save()
        return HttpResponse(f"Shortened URL: http://localhost:8000/{short_url.short_key}")

    return render(request, 'shortener/shorten_url.html', {'form': form})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
