from django.db import models

from searchfield import SearchField, add_searchfield


class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField()
    created_date = models.DateField()

    search_field = SearchField(
        source_fields=["name", "code", "created_date"],
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self) -> str:
        return self.name


@add_searchfield(search_field=["title", "category"])
class Article(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    content = models.TextField()

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self) -> str:
        return self.title
