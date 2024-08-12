from django import template

register = template.Library()


@register.filter(name="get_last_price")
def get_last_price(ans: dict, stock_name: str):

    return ans[stock_name]["lastPrice"]
