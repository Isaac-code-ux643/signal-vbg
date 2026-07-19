from django.shortcuts import render
from django.http import JsonResponse
from .models import FAQ, FAQCategory, Resource


def faq_list(request):
    categories = FAQCategory.objects.prefetch_related('questions').all()
    return render(request, 'resources/faq.html', {'categories': categories})


def chatbot_api(request):
    query = request.GET.get('query', '').lower().strip()

    if not query:
        return JsonResponse({'answer': 'Posez-moi une question sur les VBG.'})

    faqs = FAQ.objects.filter(is_published=True)
    best_match = None
    best_score = 0

    for faq in faqs:
        keywords = [k.strip().lower() for k in faq.keywords.split(',')]
        score = sum(1 for kw in keywords if kw in query)
        if score > best_score:
            best_score = score
            best_match = faq

    if best_match and best_score > 0:
        return JsonResponse({
            'question': best_match.question,
            'answer': best_match.answer,
            'category': best_match.category.name
        })

    return JsonResponse({
        'answer': "Je ne suis pas sur de comprendre. Essayez de reformuler ou "
                  "contactez le 116 (numero d'urgence)."
    })


def resource_list(request):
    resources = Resource.objects.filter(is_published=True)
    return render(request, 'resources/list.html', {'resources': resources})
