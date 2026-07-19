from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReportForm, ReportSearchForm
from .models import Report, Attachment
from .utils import detect_file_type, get_client_ip
import logging

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'reports/home.html')


def submit_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            try:
                report = form.save(commit=False)
                if not report.is_anonymous and request.user.is_authenticated:
                    report.reporter = request.user
                report.ip_address = get_client_ip(request)
                report.save()

                files = request.FILES.getlist('attachments')
                for f in files:
                    try:
                        Attachment.objects.create(
                            report=report,
                            file=f,
                            file_type=detect_file_type(f),
                            original_name=f.name,
                            file_size=f.size
                        )
                    except Exception as att_err:
                        logger.warning('Attachment save failed: %s', att_err)

                messages.success(
                    request,
                    f'Votre signalement a été enregistré. '
                    f'Votre code de suivi est : {report.tracking_code}'
                )
                return redirect('tracking:detail', code=report.tracking_code)
            except Exception as e:
                logger.error('Report save failed: %s', e)
                messages.error(request, f'Erreur lors de l\'enregistrement: {e}')
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
