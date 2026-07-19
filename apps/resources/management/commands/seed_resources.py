from django.core.management.base import BaseCommand
from apps.resources.models import FAQCategory, FAQ, Resource


class Command(BaseCommand):
    help = 'Seed FAQ and Resource data'

    def handle(self, *args, **options):
        if FAQCategory.objects.exists():
            self.stdout.write('FAQ already seeded.')
            return

        cat1 = FAQCategory.objects.create(name="Signalement", description="Comment signaler un cas de VBG", icon="exclamation-triangle", order=1)
        cat2 = FAQCategory.objects.create(name="Suivi et confidentialite", description="Suivre votre dossier et protection des donnees", icon="shield-alt", order=2)
        cat3 = FAQCategory.objects.create(name="Centres et aide", description="Trouver de l'aide pres de chez vous", icon="hospital", order=3)
        cat4 = FAQCategory.objects.create(name="Urgence", description="Que faire en cas d'urgence", icon="phone-alt", order=4)

        faqs = [
            (cat1, "Comment signaler un cas de VBG ?", "Rendez-vous sur la page 'Signaler' et remplissez le formulaire. Vous pouvez choisir de rester anonyme en cochant la case correspondante. Vous recevrez un code de suivi unique apres la soumission.", "signaler, formulaire, anonyme, anonymat", 1),
            (cat1, "Puis-je signaler de facon 100% anonyme ?", "Oui, cochez la case 'Signaler anonymement' lors de la soumission. Aucune information personnelle ne sera enregistree. Vous recevrez quand meme un code de suivi.", "anonyme, anonymat, identite, confidentialite", 2),
            (cat1, "Que se passe-t-il apres avoir soumis un signalement ?", "Votre signalement est transmis aux services competents. Vous recevez un code de suivi (ex: VBG-XXXX-XXXX) pour suivre l'avancement de votre dossier a tout moment.", "apres, suivi, suite, delai", 3),
            (cat2, "Comment suivre mon dossier ?", "Rendez-vous sur la page 'Suivre' et entrez votre code de suivi fourni lors du signalement. Vous verrez l'etat actuel de votre dossier.", "suivre, dossier, code, etat", 4),
            (cat2, "Mes donnees sont-elles protegees ?", "Oui. Toutes les donnees sont chiffrees, stockees de maniere securisee et jamais partagees avec des tiers. La confidentialite est notre priorite absolue.", "donnees, protection, chiffrement, securite", 5),
            (cat3, "Où trouver un centre d'aide ?", "Consultez la page 'Carte des centres' pour trouver les hopitaux, ONG, services sociaux et postes de police les plus proches de chez vous au Burkina Faso.", "centre, aide, carte, hopital, proche", 6),
            (cat3, "Quels sont les types de centres disponibles ?", "Nous listons les hopitaux, commissariats de police, gendarmeries, ONG specialisees, services sociaux, services juridiques et centres d'hebergement.", "types, hopital, police, ong, hebergement", 7),
            (cat4, "Que faire en cas d'urgence vitale ?", "Appelez immediatement le 116 (numero national d'urgence au Burkina Faso) ou rendez-vous au poste de police ou hopital le plus proche.", "urgence, 116, police, hopital, vital", 8),
            (cat4, "Le 116 est-il disponible 24h/24 ?", "Oui, le 116 est le numero national d'urgence du Burkina Faso, disponible 24 heures sur 24 et 7 jours sur 7.", "116, 24h, disponibilite, nuit", 9),
        ]

        for cat, q, a, kw, order in faqs:
            FAQ.objects.create(category=cat, question=q, answer=a, keywords=kw, order=order)

        resources = [
            ("Guide de prevention des VBG", "guide", "Guide complet sur la prevention des violences basees sur le genre, les signes a reconnaitre et les actions a entreprendre.", "", "", True),
            ("Brochure : Connaitre vos droits", "brochure", "Brochure informative sur les droits des victimes de VBG au Burkina Faso selon la loi.", "", "", True),
            ("Numero d'urgence national", "phone", "Appelez le 116 pour toute urgence liee a une violence. Disponible 24h/24, 7j/7.", "116", "", True),
            ("Ligne d'ecoute VBG", "phone", "Ligne d'ecoute et de conseil pour les victimes de violences basees sur le genre.", "80001112", "", True),
            ("Video : Comment reagir face a une VBG", "video", "Video informative sur les bonnes reactions face a un cas de violence basee sur le genre.", "", "https://www.youtube.com/watch?v=example", True),
            ("Ressources utiles - OMS", "link", "Page de l'OMS dediee aux violences basees sur le genre et aux ressources disponibles.", "", "https://www.who.int/health-topics/violence-against-women", True),
        ]

        for title, rtype, desc, phone, url, pub in resources:
            Resource.objects.create(title=title, resource_type=rtype, description=desc, phone_number=phone, url=url, is_published=pub)

        self.stdout.write(self.style.SUCCESS('Seeded FAQ categories, FAQs, and Resources.'))
