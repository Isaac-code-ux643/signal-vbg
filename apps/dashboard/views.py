from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from apps.reports.models import Report
from .permissions import coordinator_required


@login_required
def dashboard_home(request):
    context = {
        'total_reports': Report.objects.count(),
        'pending_reports': Report.objects.filter(status='submitted').count(),
        'resolved_reports': Report.objects.filter(status='resolved').count(),
        'critical_reports': Report.objects.filter(urgency='critical').count(),
        'total_centers': 19,
        'recent_reports': Report.objects.all()[:10],
    }
    return render(request, 'dashboard/home.html', context)


@login_required
def cases_list(request):
    qs = Report.objects.select_related('reporter').prefetch_related('attachments').all()

    status = request.GET.get('status', '')
    vbg_type = request.GET.get('type', '')
    urgency = request.GET.get('urgency', '')
    q = request.GET.get('q', '')

    if status:
        qs = qs.filter(status=status)
    if vbg_type:
        qs = qs.filter(vbg_type=vbg_type)
    if urgency:
        qs = qs.filter(urgency=urgency)
    if q:
        qs = qs.filter(
            Q(tracking_code__icontains=q) |
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    stats = {
        'total': Report.objects.count(),
        'submitted': Report.objects.filter(status='submitted').count(),
        'under_review': Report.objects.filter(status='under_review').count(),
        'in_progress': Report.objects.filter(status='in_progress').count(),
        'resolved': Report.objects.filter(status='resolved').count(),
        'closed': Report.objects.filter(status='closed').count(),
    }

    context = {
        'reports': qs[:50],
        'stats': stats,
        'current_status': status,
        'current_type': vbg_type,
        'current_urgency': urgency,
        'current_q': q,
    }
    return render(request, 'dashboard/cases.html', context)


@login_required
def case_detail(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    context = {
        'report': report,
        'history': report.status_history.all(),
        'attachments': report.attachments.all(),
    }
    return render(request, 'dashboard/case_detail.html', context)


@login_required
def case_update_status(request, report_id):
    if request.method == 'POST':
        report = get_object_or_404(Report, pk=report_id)
        new_status = request.POST.get('status', '')
        note = request.POST.get('note', '')

        valid_statuses = [s[0] for s in Report.STATUS_CHOICES]
        if new_status in valid_statuses:
            old_status = report.get_status_display()
            report.status = new_status
            report.save()

            from apps.tracking.models import StatusHistory
            StatusHistory.objects.create(
                report=report,
                old_status=old_status,
                new_status=report.get_status_display(),
                changed_by=request.user,
                comment=note,
            )

            messages.success(
                request,
                f'Statut du dossier {report.tracking_code} mis a jour : {report.get_status_display()}'
            )
        else:
            messages.error(request, 'Statut invalide.')

    return redirect('dashboard:case_detail', report_id=report_id)


@login_required
def reports_by_type(request):
    data = Report.objects.values('vbg_type').annotate(count=Count('id'))
    return JsonResponse(list(data), safe=False)


@login_required
def reports_by_month(request):
    from django.db.models.functions import TruncMonth
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
