from django.conf.urls import url
from skribblr import views

urlpatterns = [
    url(r'^compose$', views.author_portal_compose, name="Compose Portal"),
    url(r'^compose/add$', views.portal_add_entry, name="Add Entry"),
    url(r'^entry-list$', views.portal_list_entries, name="List Entries"),
    url(r'^edit/(\d+)$', views.portal_edit_entry, name="Edit Entry"),
    url(r'^edit/update/(\d+)$', views.portal_update_entry, name="Update Entry"),
    url(r'^delete/(\d+)$', views.portal_delete_entry, name="Delete Entry"),
]
