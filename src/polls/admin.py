from django.contrib import admin
from .models import User, SMS, Phone

admin.site.register(Phone)
admin.site.register(SMS)
admin.site.register(User)


# from .models import Choice, Question
#
#
# @admin.register(Choice)
# class ChoiceAdmin(admin.ModelAdmin):
#     pass
#
# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     pass

