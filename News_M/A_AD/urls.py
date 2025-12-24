from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'A_AD'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('admin-dashboard/', views.admin_dashboard , name='admin-dashboard'),

    path('gestion-annonces/', views.gestion_annonces , name='gestion-annonces'),
    path('ajouter_annonce/', views.ajouter_annonce, name='ajouter-annonce'),
    path('modifier_annonce/<int:annonce_id>', views.modifier_annonce, name='modifier-_annonce'),
    path("supprimer-annonce/<int:id>/", views.supprimer_annonce, name="supprimer-annonce"),
    path('gestion-articles/', views.gestion_articles, name='gestion-articles'),
    path('modifier-article/<int:id>', views.modifier_article, name='modifier-article'),
    path("supprimer-article/<int:id>/", views.supprimer_article, name="supprimer-article"),
    path('ajouter-article/', views.ajouter_article, name='ajouter-article'),
    path('gestion-utilisateurs/', views.gestion_utilisateurs, name='gestion-utilisateurs'),
    path('gestion-commandes', views.liste_commandes, name='gestion-commandes'),
    path('gestion-utilisateurs/supprimer/<int:user_id>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    path('ajouter_utilisateur/', views.ajouter_utilisateur, name='ajouter-utilisateur'),
    path('modifier-utilisateur/<int:user_id>', views.modifier_utilisateur, name='modifier-utilisateur'),
    path('contactez-nous/', views.contact_view, name='contactez-nous'),
    path('page-Annonces/',views.annonces_list,name='page-Annonces'),
    path('page-Articles/',views.article_list,name='page-Articles'),
    path('Article-detail/<int:article_id>/', views.article_detail, name='Article-detail'),
    path('page-contacts/', views.liste_contacts_admin, name='page-contacts'),
    path("categorie/<int:categorie_id>/", views.articles_par_categorie, name="articles_par_categorie"),
    path('commander-annonce/<int:annonce_id>', views.commander_annonce, name='commander-annonce'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)