from django.contrib.admin import BooleanFieldListFilter


class NotNullBooleanFieldListFilter(BooleanFieldListFilter):
    def choices(self, changelist):
        yield from super(NotNullBooleanFieldListFilter, self).choices(changelist)
        if self.field.null:
            yield {
                'selected': self.lookup_val2 == 'False',
                'query_string': changelist.get_query_string({self.lookup_kwarg2: 'False'}, [self.lookup_kwarg]),
                'display': 'Exists',
            }
