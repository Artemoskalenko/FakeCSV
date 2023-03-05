from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', FakeCSVMain.as_view(), name='main'),

    path('new_schema/', new_schema, name='new_schema'),
    path('<int:schema_id>/', edit_schema, name='edit_schema'),
    path('delete_schema/<int:schema_id>/', delete_schema, name='delete_schema'),

    path('<int:schema_id>/add_column/', add_column, name='add_column'),
    path('<int:schema_id>/edit_column/<int:column_id>/', edit_column, name='edit_column'),
    path('<int:schema_id>/delete_column/<int:column_id>/', delete_column, name='delete_column'),

    path('<int:schema_id>/data_sets/', data_sets_view, name='data_sets'),
    path('<int:schema_id>/data_sets/generate_data/', generate_data, name='generate_data'),

    path('logout/', logout_user, name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
