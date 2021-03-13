from . import util
from django import forms
from django.shortcuts import render
from markdown2 import Markdown
import random

# Define Markdown function
markdowner = Markdown()

# Define forms

# Form to create a new entry
class NewArticleForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(), label="Content")

# Form to edit an entry
class EditArticleForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label="Content")

# Views
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title):
    if util.get_entry(title):
        # If the entry exists, display it.
        return render(request, "encyclopedia/article.html", {
            "text": markdowner.convert(util.get_entry(title)),
            "title": title
        })
    else:
        # Else, display an error message
        return render(request, "encyclopedia/error.html", {
            "text": "Error: This entry does not exist!"
        })

def search(request):
    # Added form action="{% url 'search' %}" to layout.html
    # This is so that search logic did not have to be in every view
    query = request.GET.get('q')
    results = []

    if util.get_entry(query):
        # If search query exists, display entry
        return render(request, "encyclopedia/article.html", {
            "text": markdowner.convert(util.get_entry(query)),
            "title": query
        })
    else:
        # If it doesn't exist, search for entries title containing query
        list = util.list_entries()
        for entries in list:
            if query in entries:
                results.append(entries)
        if not results:
             # If no entries title contain query, display error
            return render(request, "encyclopedia/error.html", {
                "text": "Error: No search results for this query!"
            })
        else:
            # Else, display list of matching entries.
            return render(request, "encyclopedia/search.html", {
                "results": results
        })

def create(request):
   # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewArticleForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the items from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title):
                # If entry already exists, show error message
                return render(request, "encyclopedia/error.html", {
                    "text": "Error: This entry already exists!"
            })
            else:
                # Else, add the new entry to our encyclopedia entries
                util.save_entry(title, content)

            # Redirect user to new entry
                return render(request, "encyclopedia/article.html", {
                    "text": markdowner.convert(util.get_entry(title)),
                    "title": title
                })

   # Check if method is not POST, display the create page
    else:
        return render(request, "encyclopedia/create.html", {
        "form": NewArticleForm()
        })

def edit(request, title):
   # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = EditArticleForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the items from the 'cleaned' version of form data
            content = form.cleaned_data["content"]
            # Else, add the new entry to our encyclopedia entries
            util.save_entry(title, content)

            # Redirect user to entry
            return render(request, "encyclopedia/article.html", {
                "text": markdowner.convert(util.get_entry(title)),
                "title": title
            })

   # Check if method is not POST, display the edit page
    else:
        return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": EditArticleForm(initial={'content': util.get_entry(title)})
        })

def randompage(request):
    # Search for all existing items and select a random one.
    list = util.list_entries()
    title = random.choice(list)
    return render(request, "encyclopedia/article.html", {
        "text": markdowner.convert(util.get_entry(title)),
        "title": title
    })