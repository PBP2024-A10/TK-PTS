
from django.shortcuts import render
# from food.models import Food
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='authentication:login')
def show_main(request):
    # form = HomepageForm()
    context = {
        'page': 'homepage',
        # 'last_login': request.COOKIES['last_login'],
        'username': request.user.username,
        'pk' : request.user.pk,
        # 'foods' : Food.objects.all(),
        # 'form': form
    }
    return render(request, 'main.html', context)
