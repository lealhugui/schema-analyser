from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^rebuild_db_map/', views.rebuild_db_map),
    url(r'^db_map_view/', views.db_map_view),
    url(r'^table_pk_data/', views.tables_with_pks),
]