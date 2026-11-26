from django.shortcuts import render


def login_page(request):
    """
    Page de connexion OFFICIELLE du site.
    Le formulaire est gere en JS (fetch vers /api/auth/login/) : le JWT recu
    est stocke dans localStorage. C'est volontaire : on garde l'implementation
    la plus simple possible pour la demo Red Team (un stockage cote serveur
    en cookie httponly serait deja une amelioration de securite, qui sera
    traitee plus tard par la partie Blue Team).
    """
    return render(request, "login.html")


def register_page(request):
    return render(request, "register.html")


def dashboard_page(request):
    """
    Page protegee cote client : le JS verifie la presence d'un token dans
    localStorage puis appelle les API pour afficher les donnees.
    Aucune verification cote serveur Django (pas de session) : c'est le JWT,
    envoye par le JS, qui protege (ou pas) les donnees affichees.
    """
    return render(request, "dashboard.html")
