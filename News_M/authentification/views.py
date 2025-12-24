# authentification/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm


def admin_login_view(request):
    # إذا كان مسجلاً فليذهب إلى الdashboard
    if request.user.is_authenticated:
        return redirect('A_AD:admin-dashboard')  # تأكد اسم الـ url في a_ad.urls

    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # تحقق role بدقة (حساسية الأحرف مهمة)
                if getattr(user, 'role', '') in ['admin', 'Super_admin']:
                    login(request, user)
                    return redirect('A_AD:admin-dashboard')
                else:
                    messages.error(request, "Vous n'avez pas les droits administrateur.")
                    return redirect('authentification:admin-login')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            # debug: طباعة أخطاء الفورم (أزل أو عطل الطباعة في الإنتاج)
            print("LoginForm errors:", form.errors)
            messages.error(request, "Formulaire invalide.")
    return render(request, 'login.html', {'form': form})


# def super_admin_login_view(request):
#     if request.user.is_authenticated and getattr(request.user, 'role', '') == 'Super_admin':
#         return redirect('A_AD:gestion-utilisateurs')
#
#     form = LoginForm(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None and getattr(user, 'role', '') == 'Super_admin':
#                 login(request, user)
#                 return redirect('A_AD:gestion-utilisateurs')
#             else:
#                 messages.error(request, "Seul le Super_admin peut se connecter.")
#         else:
#             print("SuperLoginForm errors:", form.errors)
#             messages.error(request, "Formulaire invalide.")
#     return render(request, 'Super-login.html', {'form': form})

# def super_admin_login_view(request):
#     # إذا المشرف مسجل دخول مسبقاً
#     if request.user.is_authenticated and getattr(request.user, 'role', '') == 'Super_admin':
#         next_url = request.GET.get('next', 'A_AD:gestion-utilisateurs')
#         return redirect(next_url)
#
#     form = LoginForm(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None and getattr(user, 'role', '') == 'Super_admin':
#                 login(request, user)
#                 # إعادة التوجيه إلى الصفحة المطلوبة أو إدارة المستخدمين
#                 next_url = request.GET.get('next', 'A_AD:gestion-utilisateurs')
#                 return redirect(next_url)
#             else:
#                 messages.error(request, "Seul le Super_admin peut se connecter.")
#         else:
#             print("SuperLoginForm errors:", form.errors)
#             messages.error(request, "Formulaire invalide.")
#
#     return render(request, 'Super-login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('authentification:admin-login')
