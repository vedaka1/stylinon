from pathlib import Path

from jinja2 import Template
from src.domain.orders.entities import Order


def get_reset_password_template(reset_link: str) -> str:
    source = open(Path(__file__).parent / 'templates' / 'password_recovery.html', 'rb').read().decode()
    content = Template(source).render(reset_link=reset_link)
    return content


def get_new_order_template(order: Order) -> str:
    source = open(Path(__file__).parent / 'templates' / 'new_order.html', 'rb').read().decode()
    content = Template(source).render(order=order)
    return content
