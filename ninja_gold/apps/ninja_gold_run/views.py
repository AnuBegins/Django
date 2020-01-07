from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
import random

# Create your views here.

def index(request):

    if 'count' not in request.session:
        request.session['count'] = 0
    if 'color' not in request.session:
        request.session['color'] = 0
    if 'actions' not in request.session:
        request.session['actions'] = []

    if request.session['color']  == 1:
        request.session['color'] = "text-danger"
    else:
        request.session['color'] = "text-success"

    return render(request, 'ninja_gold_run/index.html')


def reset(request):
    request.session.clear()
    return redirect('/')

def getMoney(request):
    context = {
        "Grow-Op": [10,20],
        'Bordello': [5,10],
        'Dojo': [2,5],
        'Ca$ino': [0,50]
    }

    time_stamp = strftime("%B %d, %Y   |   %H:%M %p", gmtime())
    location = request.POST['getCoin']  # from the hidden form input
    if location == 'Ca$ino':
        casino_up = random.randint(0, 1)  #binary outcome: did player win or lose at casino? If win, variable = 0, else variable = 1
        request.session['color'] = casino_up

        if casino_up == 0:
            add_coins = random.randrange(1, 51)

        elif casino_up == 1:
            add_coins = random.randrange(-50,0)

        request.session['count'] += add_coins
        action = 'From the '+location+', won/lost '+ str(request.session['count']) + " pieces of gold.... "  + str(time_stamp)
        print("casino earnings: ", request.session['count'] )

        request.session['count'] = max(request.session['count'], 0)  # Assumption: ninja's cumulative gold total cannot be negative
        print("casino earnings: ", request.session['count'] )

    else:
        coin_range = context.get(location)
        add_coins = random.randrange(int(coin_range[0]), int(coin_range[1])+1 )
        request.session['count'] += add_coins
        request.session['color'] = 0
        action = 'From the '+location+', got '+ str(request.session['count']) + " pieces of gold.... "  + str(time_stamp)

    request.session['actions'].append(action)

    return redirect('/')




        # context = {
    #     "Grow-Op": '[10,20]',
    #     'Bordello': '[5,10]',
    #     'Dojo': '[2,5]',
    #     'Ca$ino': '[0,50]'
    # }

    # location = ['Grow-Op', 'Bordello', 'Dojo', 'Ca$ino']
    # coin_range = [[10,20], [5,10], [2,5], [0,50]]

    # context = {
    #     'location': location,
    #     'coin_range': coin_range
    # }

    # try:
    #     request.session['count']
    # except KeyError:
    #     request.session['count'] = 0

    # return render(request, 'ninja_gold_run/index.html', {"location" : location, "coin_range": coin_range})
