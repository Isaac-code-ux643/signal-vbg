from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReportForm, ReportSearchForm
from .models import Report, Attachment
from .utils import detect_file_type, get_client_ip


def home(request):
    return render(request, 'reports/home.html')


def submit_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            if not report.is_anonymous and request.user.is_authenticated:
                report.reporter = request.user
            report.ip_address = get_client_ip(request)
            report.save()

            files = request.FILES.getlist('attachments')
            for f in files:
                Attachment.objects.create(
                    report=report,
                    file=f,
                    file_type=detect_file_type(f),
                    original_name=f.name,
                    file_size=f.size
                )

            messages.success(
                request,
                f'Votre signalement a été enregistré. '
                f'Votre code de suivi est : {report.tracking_code}'
            )
            return redirect('tracking:detail', code=report.tracking_code)
    else:
        form = ReportForm()

    return render(request, 'reports/submit.html', {'form': form})


def search_report(request):
    form = ReportSearchForm(request.GET or None)
    if form.is_valid():
        code = form.cleaned_data['tracking_code'].upper()
        try:
            Report.objects.get(tracking_code=code)
            return redirect('tracking:detail', code=code)
        except Report.DoesNotExist:
            messages.error(request, 'Code de suivi introuvable.')

    return render(request, 'reports/search.html', {'form': form})
