from django.urls import path

from . import views
urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('notes',views.NotesView,name='notes'),
    path('delete_note/<int:pk>',views.delete_note,name='delete_note'),
    path('detail_note/<int:pk>',views.NotesDetailView.as_view(),name='detail_note'),

    path('homeworks', views.HomeworksView,name='homeworks'),
    path('update_homework/<int:pk>', views.update_homework,name='update_homework'),
    path('delete_homework/<int:pk>', views.delete_homework,name='delete_homework'),

    path('youtube', views.youtubeView,name='youtube'),

    path('todo',views.TodoView, name='todo'),
    path('update_todo/<int:pk>', views.update_todo, name='update_todo'),
    path('delete_todo/<int:pk>',views.delete_todo, name='delete_todo'),
    
    path('book',views.bookViews, name="book"),

    path('dictionary', views.DictionaryViews, name='dictionary'),

    path('wikisearch', views.WikiViews, name="wikisearch"),

    path('conversion',views.conversionViews, name="conversion"),

    path('profile',views.profileViews, name='profile'),

]