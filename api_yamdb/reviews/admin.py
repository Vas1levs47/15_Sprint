from django.contrib import admin

from reviews.models import Category, Comment, Review, Title, User


@admin.register(Title)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category', 'rating')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(User)
