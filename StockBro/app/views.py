from django.shortcuts import render

# from nsepython import nse_eq, nse_get_index_list, nse_eq_symbols, index_info, nse_list_stocks
from django.shortcuts import HttpResponse


def stock_select(request):

    return render(request, template_name="app/stock-select.html")


def stock_track(request):

    return render(request, template_name="app/stock-track.html")
