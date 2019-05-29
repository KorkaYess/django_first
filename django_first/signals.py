from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem


@receiver(post_save, sender=OrderItem)
def my_handler(sender, **kwargs):
    item = kwargs['instance']
    order = item.order
    order.price = sum(
        (item.product.price * item.quantity for item in order.items.all())
    )
