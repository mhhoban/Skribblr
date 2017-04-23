from datetime import datetime
import pytz
from django.http import HttpResponse
from django.shortcuts import redirect, render
from skribblr.models import Author, Entry

def home_page(request):
    return render(request, 'home.html')

def view_entry(request, entry_id):
    entry_id = int(entry_id)
    entry = Entry.objects.get(id=entry_id)
    return render(request, 'view-entry.html', {'entry': entry})

def author_portal_home(request):
    return render(request, 'portal-home.html')

def author_portal_compose(request):
    return render(request, 'portal-compose.html')

def portal_add_entry(request):

    # shim for early dev purposes:
    test_author = Author.objects.first()

    Entry.objects.create(
        title = request.POST['entry_title'],
        author= test_author,
        date= pytz.utc.localize(datetime.now()),
        content= request.POST['entry_content'],
        tldr = request.POST['entry_tldr']
    )

    return redirect('/portal')

def portal_list_entries(request):
    entries = Entry.objects.all()
    return render(request, 'portal-list.html', {'entries': entries})

def portal_edit_entry(request, entry_id):
    entry = Entry.objects.get(id=int(entry_id))
    return render(request, 'portal-edit.html', {'entry': entry})

def portal_update_entry(request, entry_id):
    entry_id = int(entry_id)
    entry = Entry.objects.filter(id=entry_id).first()

    entry.title = request.POST['updated_title']
    entry.content = request.POST['updated_content']
    entry.tldr = request.POST['updated_tldr']
    entry.save()

    return render(request, 'portal-home.html')

def portal_delete_entry(request, entry_id):
    """
    Delete entry with PK entry_id from DB
    """

    if request.method != 'POST':
        return(HttpResponse(status=404))

    else:
        try:
            entry = Entry.objects.get(id=entry_id)
        except DoesNotExist:
            return(HttpResponse(status=404))
        if(entry.delete()):
            return redirect('/portal/entry-list')
