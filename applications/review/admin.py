from django.contrib import admin

from applications.review.models import Review, Like

admin.site.register(Review)
admin.site.register(Like)
