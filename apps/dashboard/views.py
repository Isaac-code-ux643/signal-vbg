from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from apps.reports.models import Report
from apps.centers.models import SupportCenter


@login_required
def dashboard_home(request):
    context = {
        'total_reports': Report.objects.count(),
        'pending_reports': Report.objects.filter(status='submitted').count(),
        'resolved_reports': Report.objects.filter(status='resolved').count(),
        'critical_reports': Report.objects.filter(urgency='critical').count(),
        'total_centers': SupportCenter.objects.filter(is_active=True).count(),
        'recent_reports': Report.objects.all()[:10],
    }
    return render(request, 'dashboard/home.html', context)


@login_required
def reports_by_type(request):
    data = Report.objects.values('vbg_type').annotate(count=Count('id'))
    return JsonResponse(list(data), safe=False)


@login_required
def reports_by_month(request):
    data = (
        Report.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    result = [{'month': item['month'].isoformat(), 'count': item['count']} for item in data]
    return JsonResponse(result, safe=False)


@login_required
def reports_by_status(request):
    data = Report.objects.values('status').annotate(count=Count('id'))
    return JsonResponse(list(data), safe=False)
