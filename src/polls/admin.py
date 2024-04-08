from django.contrib import admin
from .models import User, SMS, Phone, SmsConversation,SMSReceived,SurveyQuestion,Survey,Account,SMSSent,SMSQueue

admin.site.register(Phone)
admin.site.register(SMS)
admin.site.register(SmsConversation)
admin.site.register(SMSReceived)
admin.site.register(SurveyQuestion)
admin.site.register(Survey)
admin.site.register(Account)
admin.site.register(SMSSent)
admin.site.register(SMSQueue)
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

