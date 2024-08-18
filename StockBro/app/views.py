from django.shortcuts import render, HttpResponse

from nsepython import nse_eq, nse_eq_names_symbols, nse_eq_names
from asgiref.sync import sync_to_async
from threading import Thread
from collections import deque

import time
import json
import pandas as pd

from .models import Stockdeatils
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@sync_to_async
def checkAuthenticated(request):

    return request.user.is_authenticated


@login_required
def stock_select(request):

    print(request.user.username)
    stock_names = nse_eq_names_symbols()
    # print(stock_names)
    return render(request, template_name="app/stock-select.html", context={
        "stock_names": stock_names
    })


async def stock_track(request):

    logged_in = await checkAuthenticated(request)

    if not logged_in:
        return redirect("authy:login")

    stock_names = request.GET.getlist('stockpicker')
    print(stock_names)
    que = deque()
    threads = list()

    # Iterate over all stocks and create a new thread
    for index in range(len(stock_names)):

        thread = Thread(target=lambda que,
                        stock_name: que.append({stock_name:
                                                nse_eq(stock_name)}),
                        args=(que, stock_names[index]))

        threads.append(thread)
        thread.start()

    # Execute all threads
    for thread in threads:

        thread.join()

    ans = list()
    while que:

        stock = que.popleft()

        # Get the first key i.e. symbol of stock
        symbol = next(iter(stock))

        # Get rest attributes
        companyName = stock[symbol]["info"]["companyName"]
        industry = stock[symbol]["info"]["industry"]
        prevClose = stock[symbol]["priceInfo"]["previousClose"]
        lastPrice = stock[symbol]["priceInfo"]["lastPrice"]
        percentChange = ((lastPrice - prevClose)/lastPrice)*100
        lowerCircuit = stock[symbol]["priceInfo"]["lowerCP"]
        upperCircuit = stock[symbol]["priceInfo"]["upperCP"]

        # Check wheather an stock_object of same symbol exists or not symbols should be unique
        stock_object = Stockdeatils.objects.filter(
            symbol__iexact=symbol).first()

        # If no objects exists
        if stock_object is None:

            # Create an stock_object if it doesn't exists
            stock_object = Stockdeatils(symbol=symbol, companyName=companyName,
                                        industry=industry, prevClose=prevClose,
                                        lastPrice=lastPrice, percentChange=percentChange,
                                        lowerCircuit=lowerCircuit, upperCircuit=upperCircuit)
        else:

            # Do update the stock_object if it already exists
            stock_object.lowerCircuit = lowerCircuit
            stock_object.upperCircuit = upperCircuit
            stock_object.prevClose = prevClose
            stock_object.lastPrice = lastPrice
            stock_object.percentChange = percentChange

        # Persists change into the db
        stock_object.save()

        ans.append(stock_object)

    return render(request,
                  template_name='app/stock-view.html',
                  context={
                      'data': ans,
                      'room_name': 'track',
                      'selectedstock': stock_names
                  })
