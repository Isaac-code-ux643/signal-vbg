from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.reports.models import Report


def track_by_code(request):
    if request.method == 'POST':
        code = request.POST.get('tracking_code', '').strip().upper()
        if code:
            try:
                Report.objects.get(tracking_code=code)
                return redirect('tracking:detail', code=code)
            except Report.DoesNotExist:
                messages.error(request, 'Code de suivi introuvable.')
    return render(request, 'tracking/search.html')


def track_report(request, code):
    report = get_object_or_404(Report, tracking_code=code.upper())
    context = {
        'report': report,
        'history': report.status_history.all(),
        'attachments': report.attachments.all(),
    }
    return render(request, 'tracking/detail.html', context)
