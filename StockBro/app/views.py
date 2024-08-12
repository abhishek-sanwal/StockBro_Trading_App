from django.shortcuts import render


from nsepython import nse_eq, nse_eq_names_symbols, nse_eq_symbols

from django.shortcuts import HttpResponse

from threading import Thread
from queue import Queue

import time


def stock_select(request):

    stock_names = nse_eq_names_symbols()
    print(stock_names, "There are all stocks")
    return render(request, template_name="app/stock-select.html", context={
        "stock_names": stock_names
    })


def stock_track(request):

    stock_names = request.GET.getlist('stockpicker')
    ans = dict()

    # print(stock_names)

    # startTime =  time.time()

    # for stock in stock_names:

    #     nse_eq(stock)

    # endTime = time.time()

    # print("Total time taken by normal process is", endTime - startTime)

    startTime = time.time()
    # Multithreading with Queue to perform more efficiently.
    que = Queue()
    # Thread Pool
    threads = list()

    # Iterate over all stocks and create a new thread
    for index in range(len(stock_names)):

        thread = Thread(target=lambda que,
                        stock_name: que.put({stock_name: nse_eq(stock_name)}),
                        args=(que, stock_names[index]))
        threads.append(thread)
        thread.start()

    # Execute all threads
    for thread in threads:

        thread.join()

    while que:

        item = que.get()
        ans.update(item)

    endTime = time.time()

    print("Total time taken by multithreading approach is ", endTime - startTime)

    return render(request, template_name="app/stock-track.html", context={
        "data", ans
    })
