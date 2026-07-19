from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import SupportCenter


def centers_map(request):
    centers = SupportCenter.objects.filter(is_active=True)
    return render(request, 'centers/map.html', {'centers': centers})


def centers_json(request):
    centers = SupportCenter.objects.filter(is_active=True).values(
        'id', 'name', 'center_type', 'latitude', 'longitude',
        'address', 'phone', 'services_offered', 'opening_hours'
    )
    return JsonResponse(list(centers), safe=False)


def center_detail(request, pk):
    center = get_object_or_404(SupportCenter, pk=pk, is_active=True)
    return render(request, 'centers/detail.html', {'center': center})
