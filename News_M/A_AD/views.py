
from itertools import cycle
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.views import LogoutView
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import Permission
from .forms import CommanderAnnonceForm, AnnonceForm
from .models import Article, Annonce, ActionLog, ContactMessage, Categorie, CommandeAnnonce

User = get_user_model()


# ================== Decorators ==================

def super_admin_required(view_func):
    """تحقق من أن المستخدم Super_admin"""
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'Super_admin':
            messages.error(request, "Vous n’avez pas la permission.")
            return redirect('authentification:admin-login')
        return view_func(request, *args, **kwargs)
    return wrapper


def permission_or_super_admin(permission_codename, login_url='/auth/admin-login/'):
    """تحقق من الصلاحية أو تجاوزها إذا كان Super_admin"""
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role == 'Super_admin' or request.user.has_perm(permission_codename):
                return view_func(request, *args, **kwargs)
            messages.error(request, "Vous n’avez pas la permission ")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        return _wrapped_view
    return decorator


def filter_by_query(query, queryset, fields):
    """فلترة QuerySet حسب نص البحث"""
    if query:
        q_objects = Q()
        for field in fields:
            q_objects |= Q(**{f"{field}__icontains": query})
        queryset = queryset.filter(q_objects)
    return queryset


# ================== Home Page ==================

def home(request):
    query = request.GET.get('q')

    # Articles
    article_list = filter_by_query(query, Article.objects.all().order_by('-date_pub'), ["titre", "contenu"])
    article_paginator = Paginator(article_list, 5)
    page_articles = request.GET.get('article_page')
    articles = article_paginator.get_page(page_articles)

    # Annonces
    annonce_list = filter_by_query(query, Annonce.objects.all().order_by('-date_pub'), ["titre", "description"])
    annonce_paginator = Paginator(annonce_list, 3)
    page_annonces = request.GET.get('annonce_page')
    annonces = annonce_paginator.get_page(page_annonces)

    # Catégories avec couleurs
    categories = Categorie.objects.all()
    colors = ["primary", "success", "danger", "warning", "info"]
    categories_with_colors = [(cat, colors[i % len(colors)]) for i, cat in enumerate(categories)]

    return render(request, 'home.html', {
        'articles': articles,
        'annonces': annonces,
        'categories': categories_with_colors,
        'query': query,
    })


# ================== Dashboard ==================

@never_cache
@login_required(login_url='/auth/admin-login/')
def admin_dashboard(request):
    nb_articles = Article.objects.count()
    nb_annonces = Annonce.objects.count()
    nb_users = User.objects.count()
    last_actions = ActionLog.objects.order_by('-date')[:10]
    context = {
        'nb_articles': nb_articles,
        'nb_annonces': nb_annonces,
        'nb_users': nb_users,
        'last_actions': last_actions
    }
    return render(request, 'admin-dashboard.html', context)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('authentification:admin-login')


# ================== Gestion Annonces ==================

@never_cache
@login_required
@permission_or_super_admin('A_AD.view_annonce')
def gestion_annonces(request):
    annonces = Annonce.objects.all()
    return render(request, 'gestion-annonces.html', {'annonces': annonces})


@never_cache
@login_required
@permission_or_super_admin('A_AD.add_annonce')
def ajouter_annonce(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        prix = request.POST.get('prix')
        image = request.FILES.get('image')
        annonce = Annonce.objects.create(titre=titre, description=description, prix=prix, image=image)
        ActionLog.objects.create(user=request.user, action=f"Ajout de l'annonce '{annonce.titre}'")
        messages.success(request, "Annonce ajoutée avec succès !")
        return redirect('A_AD:gestion-annonces')
    return render(request, 'ajouter_annonce.html')


@never_cache
@login_required
@permission_or_super_admin('A_AD.change_annonce')
def modifier_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES, instance=annonce)
        if form.is_valid():
            form.save()
            ActionLog.objects.create(user=request.user, action=f"Modification de l'annonce '{annonce.titre}'")
            messages.success(request, "Annonce modifiée avec succès !")
            return redirect('A_AD:gestion-annonces')
    else:
        form = AnnonceForm(instance=annonce)
    return render(request, 'modifier_annonce.html', {'form': form})


@never_cache
@login_required
@permission_or_super_admin('A_AD.delete_annonce')
def supprimer_annonce(request, id):
    annonce = get_object_or_404(Annonce, id=id)
    titre = annonce.titre
    annonce.delete()
    ActionLog.objects.create(user=request.user, action=f"Suppression de l'annonce '{titre}'")
    messages.success(request, "Annonce supprimée avec succès !")
    return redirect("A_AD:gestion-annonces")


# ================== Gestion Articles ==================

@never_cache
@login_required
@permission_or_super_admin('A_AD.view_article')
def gestion_articles(request):
    articles = Article.objects.all()
    return render(request, 'gestion-articles.html', {'articles': articles})


@never_cache
@login_required
@permission_or_super_admin('A_AD.add_article')
def ajouter_article(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.POST.get('description')
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        article = Article.objects.create(titre=titre, contenu=contenu, image=image, video=video)
        ActionLog.objects.create(user=request.user, action=f"Ajout de l'article '{article.titre}'")
        messages.success(request, "Article ajouté avec succès !")
        return redirect('A_AD:gestion-articles')
    return render(request, 'ajouter_article.html')


@never_cache
@login_required
@permission_or_super_admin('A_AD.change_article')
def modifier_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        article.titre = request.POST.get("titre")
        article.contenu = request.POST.get("contenu")
        if request.FILES.get("image"):
            article.image = request.FILES["image"]
        if request.FILES.get("video"):
            article.video = request.FILES["video"]
        article.save()
        ActionLog.objects.create(user=request.user, action=f"Modification de l'article '{article.titre}'")
        messages.success(request, "Article modifié avec succès !")
        return redirect("A_AD:gestion-articles")
    return render(request, "modifier_article.html", {"article": article})


@never_cache
@login_required
@permission_or_super_admin('A_AD.delete_article')
def supprimer_article(request, id):
    article = get_object_or_404(Article, id=id)
    titre = article.titre
    article.delete()
    ActionLog.objects.create(user=request.user, action=f"Suppression de l'article '{titre}'")
    messages.success(request, "Article supprimé avec succès !")
    return redirect("A_AD:gestion-articles")


# ================== Gestion Utilisateurs ==================

@never_cache
@login_required
@permission_or_super_admin('auth.view_user')
def gestion_utilisateurs(request):
    utilisateurs = User.objects.all()
    return render(request, 'gestion-utilisateurs.html', {'utilisateurs': utilisateurs})


@never_cache
@login_required
@permission_or_super_admin('auth.add_user')
def ajouter_utilisateur(request):
    permissions = Permission.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        perms_selected = request.POST.getlist('permissions')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Nom d’utilisateur déjà utilisé !")
        else:
            utilisateur = User.objects.create_user(username=username, email=email, password=password, role=role)
            for perm_id in perms_selected:
                perm = Permission.objects.get(id=perm_id)
                utilisateur.user_permissions.add(perm)
            ActionLog.objects.create(user=request.user, action=f"Ajout de l'utilisateur '{username}'")
            messages.success(request, "Utilisateur ajouté avec succès !")
            return redirect('A_AD:gestion-utilisateurs')
    return render(request, 'ajouter_utilisateur.html', {'permissions': permissions})


@never_cache
@login_required
@permission_or_super_admin('auth.change_user')
def modifier_utilisateur(request, user_id):
    utilisateur = get_object_or_404(User, id=user_id)
    all_permissions = Permission.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')
        selected_perms = request.POST.getlist('permissions')
        if User.objects.exclude(id=user_id).filter(username=username).exists():
            messages.error(request, "Nom d’utilisateur déjà utilisé !")
        else:
            ancien_username = utilisateur.username
            ancien_email = utilisateur.email
            utilisateur.username = username
            utilisateur.email = email
            utilisateur.role = role
            if password:
                utilisateur.set_password(password)
            utilisateur.save()
            utilisateur.user_permissions.set(selected_perms)
            ActionLog.objects.create(
                user=request.user,
                action=f"Modification de l'utilisateur '{ancien_username}' → '{username}', rôle: {role}, email: {ancien_email} → {email}"
            )
            messages.success(request, "Utilisateur modifié avec succès !")
            return redirect('A_AD:gestion-utilisateurs')
    return render(request, 'modifier_utilisateur.html', {
        'utilisateur': utilisateur,
        'all_permissions': all_permissions
    })


@never_cache
@login_required
@permission_or_super_admin('auth.delete_user')
def supprimer_utilisateur(request, user_id):
    utilisateur = get_object_or_404(User, id=user_id)
    username = utilisateur.username
    utilisateur.delete()
    ActionLog.objects.create(user=request.user, action=f"Suppression de l'utilisateur '{username}'")
    messages.success(request, "Utilisateur supprimé avec succès !")
    return redirect('A_AD:gestion-utilisateurs')


# ================== Gestion Contacts ==================

def contact_view(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        email = request.POST.get("email")
        sujet = request.POST.get("sujet")
        message = request.POST.get("message")
        ContactMessage.objects.create(nom=nom, email=email, sujet=sujet, message=message)
        messages.success(request, "Votre message a été envoyé avec succès ✅")
        return redirect('A_AD:contactez-nous')
    return render(request, 'contactez-nous.html')


@login_required
@permission_or_super_admin('A_AD.view_contactmessage')
def liste_contacts_admin(request):
    contacts = ContactMessage.objects.all().order_by('-date_envoi')
    return render(request, 'page-contacts.html', {'contacts': contacts})


# ================== Déconnexion ==================

def deconnexion(request):
    logout(request)
    return redirect('authentification:admin-login')


# ================== Pages publiques ==================

def annonces_list(request):
    annonces = Annonce.objects.all().order_by('-date_pub')
    return render(request, 'page-Annonces.html', {'annonces': annonces})


def article_list(request):
    articles_list = Article.objects.all()
    paginator = Paginator(articles_list, 4)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    return render(request, 'page-articles.html', {'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'article_detail.html', {'article': article})


def articles_par_categorie(request, categorie_id):
    categories = Categorie.objects.all()
    colors = ["primary", "success", "danger", "warning", "info"]
    categories_with_colors = [(cat, colors[i % len(colors)]) for i, cat in enumerate(categories)]
    categorie = get_object_or_404(Categorie, id=categorie_id)
    articles = Article.objects.filter(categorie=categorie)
    return render(request, "articles_par_categorie.html", {
        "categories": categories_with_colors,
        "categorie": categorie,
        "articles": articles
    })


def redirect_to_dashboard(request):
    return redirect('A_AD:home')


def commander_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    if request.method == "POST":
        form = CommanderAnnonceForm(request.POST)
        if form.is_valid():
            commande = form.save(commit=False)
            commande.annonce = annonce
            commande.save()
            messages.success(request, "✅ Votre commande a été enregistrée avec succès !")
            form = CommanderAnnonceForm()
    else:
        form = CommanderAnnonceForm()
    return render(request, "commander_annonce.html", {
        "form": form,
        "annonce": annonce
    })


@never_cache
@login_required
@permission_or_super_admin('A_AD.view_commandeannonce')
def liste_commandes(request):
    commandes = CommandeAnnonce.objects.all().order_by('-date_commande')
    return render(request, 'gestion-commandes.html', {'commandes': commandes})

