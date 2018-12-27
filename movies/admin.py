from django.contrib import admin

from .models import Poll, Answer


class AnswerInline(admin.TabularInline):
    model = Poll.answers.through
    extra = 5


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['poll_question']}),
        ('Date information', {'fields': ['poll_date']}),
    ]
    inlines = (AnswerInline,)


class AnswerAdmin(admin.ModelAdmin):
    fields = ('answer_text',)


admin.site.register(Poll, PollAdmin)
admin.site.register(Answer, AnswerAdmin)
