import random

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import generic

from django.contrib.auth.decorators import login_required

import wikipedia
import requests
from youtubesearchpython import VideosSearch
from .forms import *
# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/home.html')

#NOTES-----------------------------------------------------
@login_required
def NotesView(request):
    if request.method == "POST":
        form = NotesForms(request.POST)
        if form.is_valid:
            notes = NotesModel(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request, f"Notes of {request.user} added successfully!")

        return HttpResponseRedirect(reverse('notes'))
    else:
        form = NotesForms()
    notes = NotesModel.objects.filter(user=request.user)
    context = {
        'notes' : notes,
        'form' : form,
    }
    return render(request, 'notes/notes_new.html', context)
@login_required
def delete_note(request, pk=None):
    NotesModel.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = NotesModel
    template_name = "notes/notes_detail_new.html"
    context_object_name = 'notes'

#HOMEWORK----------------------------------------
@login_required
def HomeworksView(request):
    if request.method == 'POST':
        form = HomeworksForms(request.POST)
        try:
            finished = request.POST['is_finished']
            if finished == 'on':
                finished = True
            else:
                finished = False
        except:
            finished = False
        homework = HomeworkModels(
            user = request.user,
            subject = request.POST['subject'],
            title = request.POST['title'],
            description = request.POST['description'],
            due = request.POST['due'],
            is_finished = finished
            
        )
        homework.save()
        messages.success(request, f"Homework Added from {request.user.username}!")
        return HttpResponseRedirect(reverse('homeworks'))
    else:
        form = HomeworksForms()
    homeworks = HomeworkModels.objects.filter(user=request.user)
    homeworks_done = False
    if len(homeworks) == 0:
        homeworks_done == True
    else:
        homeworks_done
    context = {
        'homeworks' : homeworks,
        'homeworks_done' : homeworks_done,
        'form' : form,
    }
    return render(request, 'homework/homework_new.html', context)
@login_required
def update_homework(request, pk=None):
    homework = HomeworkModels.objects.get(id=pk)
    #default value is false and if put an if statement, the object which is false is true
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save() 
    return redirect('homeworks')

def delete_homework(request, pk=None):
    HomeworkModels.objects.get(id=pk).delete()
    return redirect('homeworks')


#Youtube.......................................................

def youtubeView(request):
    if request.method == "POST":
        form = YoutubeForms(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input' : text,
                'title' : i['title'],
                'duration' : i['duration'],
                'thumbnail' : i['thumbnails'][0]['url'],
                'channel' : i['channel']['name'],
                'link' : i['link'],
                'views' : i['viewCount']['short'],
                'published' : i['publishedTime']
                
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form' : form,
                'results' : result_list
            }
        return render(request, 'youtube/youtube_new.html', context)
    else:
        form = YoutubeForms()
    context = {
        'form' : form
    }
    return render(request, 'youtube/youtube_new.html', context)
@login_required
def TodoView(request):
    if request.method == "POST":
        form = TodoForms(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = TodoModel(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request, f"To-do added successfully from {request.user.username}")
            return HttpResponseRedirect(reverse('todo'))
    else:
        form = TodoForms()
    todo = TodoModel.objects.filter(user=request.user)
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {
        'todos': todo,
        'form': form,
        'todo_done': todo_done
    }
    return render(request, 'todo/todo_new.html',context)
@login_required
def update_todo(request, pk=None):
    todo = TodoModel.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')
@login_required
def delete_todo(request, pk=None):
    todo = TodoModel.objects.get(id=pk).delete()
    return redirect('todo')

#book.....................................................
@login_required
def bookViews(request):
    if request.method == 'POST':
        form = BookForms(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'book/books_new.html', context)
    else:
        form = BookForms()
    context = {
        'form': form
    }
    return render(request, 'book/books_new.html', context)

#Dictionary..........................................................

def DictionaryViews(request):
    if request.method == "POST":
        form = DictionaryForms(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text'],
            audio = answer[0]['phonetics'][0]['audio'],
            definition = answer[0]['meanings'][0]['definitions'][0]['definition'],
            example = answer[0]['meanings'][0]['definitions'][0]['example'],
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms
            }
        except:
            context = {
                'form': form,
                'input': ''
            }
        return render(request, 'dictionary/dictionary_new.html', context)
    else:
        form = DictionaryForms()
    context = {
        'form': form
    }
    return render(request, 'dictionary/dictionary_new.html', context)

#WIKI...................................................................

def WikiViews(request):
    if request.method == "POST":
        form = WikiForms(request.POST)
        text = request.POST['text']
        try:
            search = wikipedia.page(str(text))
        except wikipedia.DisambiguationError as e:
            new_search = random.choice(e.options)
            search = wikipedia.page(str(new_search))
        context = {
            'form' : form,
            'title' : search.title,
            'url' : search.url,
            'summary' : search.summary
        }
        return render(request, 'wiki/wiki_new.html', context)
    else:
        form = WikiForms()
        context = {
            'form' : form
        }
    return render(request, 'wiki/wiki_new.html', context)

#conversion..................................................

def conversionViews(request):
    if request.method == 'POST':
        form = ConversionForms(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForms()
            context = {
                'form' : form,
                'm_form' : measurement_form,
                'input' : True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f"{input} yard = {int(input)*3} foot"
                    if first == 'foot' and second == 'yard':
                        answer = f"{input} foot = {int(input)/3} yard"
                context = {
                    'form' : form,
                    'm_form' : measurement_form,
                    'input' : True,
                    'answer' : answer,
                }
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForms()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilograms':
                        answer = f"{input} pound = {int(input) * 0.453592} kg"
                    if first == 'kilograms' and second == 'pound':
                        answer = f"{input} kg = {int(input) / 2.2062} pound"
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer,
                }

    else:
        form = ConversionForms()
        context = {
        'form' : form,
         }
    return render(request, 'conversion/conversion_new.html', context)

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"{username} has signed up successfully!")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
        'form' : form
    }
    return render(request, 'register_new.html', context)

@login_required
def profileViews(request):
    homework = HomeworkModels.objects.filter(is_finished = False, user = request.user)
    todo = TodoModel.objects.filter(is_finished=False, user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {
        'homeworks' : homework,
        'todos' : todo,
        'homeworks_done' : homework_done,
        'todo_done' : todo_done
    }
    return render(request, 'profile_new.html', context)

