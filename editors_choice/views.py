from django.shortcuts import render

# Create your views here.
def show_index_er(request):
    context = {}
    return render(request, 'editors_choice.html', context)