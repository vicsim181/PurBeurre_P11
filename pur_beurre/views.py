from django.views.defaults import page_not_found


def handler404_view(request, exception, template_name='page_not_found.html'):
    return page_not_found(request, exception, template_name)
