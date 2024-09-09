from django import template

register = template.Library()


@register.filter
def get_total_price(orders):
    return sum(order.total_price for order in orders)
