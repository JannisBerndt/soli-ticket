from django import template

register = template.Library()

@register.filter
def setHTMLAttributes(self, string_dict):
    attributes = eval(string_dict)
    for attribute in attributes:
        self.field.widget.attrs[attribute] = attributes[attribute]
    return self

@register.filter
def test(self):
    print('IT WORKED')
    return self
