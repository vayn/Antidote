from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import list_detail
from django.http import HttpResponse
from django.template import loader, Context
from antidote.red.models import Entry
from antidote.red.forms import UploadFileForm
from antidote.utils.util import markdown_factory

def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Enter at most 20 characters.')
        else:
            entries = Entry.objects.filter(title__icontains=q)
            return render_to_response('search_result.html',
                                      {'entries': entries, 'query': q,})
    return render_to_response('index.html', {'errors': errors})

def entry_detail(request, entry_id):
    pass

def _handle_uploaded_file(filename, mkdfile):
    response = HttpResponse(mimetype='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s.mkd' % filename

    t = loader.get_template('sample.mkd')
    c = Context(mkdfile)
    response.write(t.render(c))
    return response

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filename, mkdfile = markdown_factory(request.FILES['content'], request.POST)
            return _handle_uploaded_file(filename, mkdfile)
    else:
        form = UploadFileForm()
    return render_to_response('index.html', {'form': form})

def export(request, entry_id):
    e = get_object_or_404(Entry, id=entry_id)

    filename = e.title.replace(' ', '-').lower()
    for p in '{}':
        filename = filename.replace(p, '')
    for tag in e.tags.all():
        e.taglist.append(tag.name)
    filename = str(e.pub_date) + '-' + filename

    exp = {'title': e.title,
           'taglist': e.taglist,
           'pub_date': e.pub_date,
           'content': e.content,
          }
    return _handle_uploaded_file(filename, exp)
