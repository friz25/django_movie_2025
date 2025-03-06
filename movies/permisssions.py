from django.http import Http404
from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        """ проверка (этот) юзер = суперЮзер? """
        return bool(request.user and request.user.is_superuser)

# class AuthorPermissionsMixin:
#     def has_permissions(self):
#         """ проверка (этот) юзер = автор (этого) поста? """
#         return self.get_object().author == self.request.user
#
#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_permissions():
#             """ если юзер не автор этого поста ТО error404"""
#             raise Http404()
#         return super().dispatch(request, *args, **kwargs)
#
# class MembersPermissionsMixin(AuthorPermissionsMixin):
#     def has_permissions(self):
#         """ проверка (этот) юзер = member (этой) статьи? """
#         return self.request.user in self.get_object().members.all()