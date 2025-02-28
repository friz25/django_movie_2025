INSTALLED_APPS = [
        'modeltranslation',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'django.contrib.flatpages',

        'rest_framework',
        'rest_framework.authtoken', # [10] auth/регистрация
        'rest_framework_json_api', # [17] jwt

        'ckeditor',
        'ckeditor_uploader',  # чтоб (через ckeditor) загружать img'ы
        'snowpenguin.django.recaptcha3',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.vk',
        # 'allauth.socialaccount.providers.google',
        # 'allauth.socialaccount.providers.facebook',
        # 'allauth.socialaccount.providers.discord',
        # 'allauth.socialaccount.providers.steam',

        'djoser', # [10] auth/регистрация
        'drf_yasg', #[12] автодок-я swagger/redoc (drf-yasg)
        'oauth2_provider', #[13] вход через VK
        'social_django', #[13] вход через VK
        'rest_framework_social_oauth2', #[13] вход через VK
        'django_filters', #[9] фильтр
        'corsheaders', #[15]

        'movies',
        'contact',

    ]

# def set_installed_apps():
#     INSTALLED_APPS = [
#         'modeltranslation',
#         'django.contrib.admin',
#         'django.contrib.auth',
#         'django.contrib.contenttypes',
#         'django.contrib.sessions',
#         'django.contrib.messages',
#         'django.contrib.staticfiles',
#         'django.contrib.sites',
#         'django.contrib.flatpages',
#
#         'rest_framework',
#         'rest_framework.authtoken',
#
#         'ckeditor',
#         'ckeditor_uploader',  # чтоб (через ckeditor) загружать img'ы
#         'snowpenguin.django.recaptcha3',
#         'allauth',
#         'allauth.account',
#         'allauth.socialaccount',
#         'allauth.socialaccount.providers.vk',
#         # 'allauth.socialaccount.providers.google',
#         # 'allauth.socialaccount.providers.facebook',
#         # 'allauth.socialaccount.providers.discord',
#         # 'allauth.socialaccount.providers.steam',
#
#         # 'djoser',
#         'drf_yasg',
#         'django_filters',
#         'corsheaders',
#
#         'movies',
#         'contact',
#
#     ]
#     return INSTALLED_APPS