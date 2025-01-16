from django.contrib import admin
from . import models


admin.site.register(
    [
        models.Post,
        models.Comment,
        models.PostLike,
    ]
)
