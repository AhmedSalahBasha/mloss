"""
URLConf for software.

Recommended usage is to use a call to ``include("software.urls")`` in your project's
root URLConf to include this URLConf for any URL beginning with
'/browse/'.

"""

from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from models import Author, Software
from views import entry


# Info for generic views.
base_generic_dict = {
    'paginate_by': 10,
    }

software_info_dict = dict(base_generic_dict,
                          queryset=Software.objects.all(),
                          template_name='software_list.html')

software_info_dict_date = dict(base_generic_dict,
		queryset=Software.objects.all().order_by('-pub_date'),
		template_name='software_list.html')

software_info_dict_software = dict(base_generic_dict,
		queryset=Software.objects.all().order_by('-title'),
		template_name='software_list.html')

software_info_dict_author = dict(base_generic_dict,
		queryset=Software.objects.all().order_by('-authors'),
		template_name='software_list.html')

software_info_dict_tags = dict(base_generic_dict,
		queryset=Software.objects.all().order_by('-keyword1'),
		template_name='software_list.html')

software_info_dict_license = dict(base_generic_dict,
		queryset=Software.objects.all().order_by('-os_license'),
		template_name='software_list.html')

#author_info_dict = dict(base_generic_dict,
#                        queryset=Author.objects.all(),
#                        template_name='author_list.html')
#
# General softwares views.
urlpatterns = patterns('',
                       (r'^(?P<software_id>\d+)/$', entry.software_detail),
                       )

# Generic views.
urlpatterns += patterns('',
                        (r'^$', object_list, software_info_dict),
                        (r'^date/$', object_list, software_info_dict_date),
                        (r'^software/$', object_list, software_info_dict_software),
                        (r'^author/$', object_list, software_info_dict_author),
                        (r'^tags/$', object_list, software_info_dict_tags),
                        (r'^license/$', object_list, software_info_dict_license),
                        )
