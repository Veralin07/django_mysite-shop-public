from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Product

class LatestProductsFeed(Feed):
    title = "Latest Products"
    link = "/products/"
    description = "Updates on the latest products."

    def items(self):
        return Product.objects.order_by('-created_at')[:10]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()
