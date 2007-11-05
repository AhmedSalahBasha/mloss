from django.views.generic import list_detail
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from software.models import Software
from software.models import Author, Tag, License, Language, OpSys



def software_by_user(request, username):
    """
    List of Software submitted by a particular User.
    """
    user = get_object_or_404(User, username__exact=username)
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=Software.objects.get_by_submitter(user.username),
                                   extra_context={ 'object': user },
                                   template_name='software/software_list.html'
                                   )

def software_by_author(request, slug):
    """
    List of software with a particular Author
    """
    author = get_object_or_404(Author, slug__exact=slug)
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=Software.objects.get_by_author(author.slug),
                                   extra_context={ 'object':author },
                                   template_name='software/software_list.html',
                                   )

def software_by_tag(request, slug):
    """
    List of software with a particular Tag
    """
    tag = get_object_or_404(Tag, slug__exact=slug)
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=Software.objects.get_by_tag(tag.slug),
                                   extra_context={ 'object':tag },
                                   template_name='software/software_list.html',
                                   )

def software_by_license(request, slug):
    """
    List of software with a particular License
    """
    lic = get_object_or_404(License, slug__exact=slug)
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=Software.objects.get_by_license(lic.slug),
                                   extra_context={ 'object':lic },
                                   template_name='software/software_list.html',
                                   )

def software_by_language(request, slug):
    """
    List of software with a particular Language
    """
    language = get_object_or_404(Language, slug__exact=slug)
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=Software.objects.get_by_language(language.slug),
                                   extra_context={ 'object':language },
                                   template_name='software/software_list.html',
                                   )

def software_by_opsys(request, slug):
    """
    List of software with a particular Operating System
    """
    opsys = get_object_or_404(OpSys, slug__exact=slug)
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=Software.objects.get_by_opsys(opsys.slug),
                                   extra_context={ 'object':opsys },
                                   template_name='software/software_list.html',
                                   )

def software_by_date(request):
    """
    List of Software ranked by date
    """

    softwarelist = Software.objects.all().order_by('-pub_date')

    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=softwarelist,
                                   template_name='software/software_list.html',
                                   )

def software_by_title(request):
    """
    List of Software ranked by date
    """

    softwarelist = Software.objects.all().order_by('title')

    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=softwarelist,
                                   template_name='software/software_list.html',
                                   )

def software_by_views(request):
    """
    List of Software ranked by vies
    """

    softwarelist = Software.objects.all().order_by('-total_number_of_views')

    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=softwarelist,
                                   template_name='software/software_list.html',
                                   )
def software_by_downloads(request):
    """
    List of Software ranked by downloads
    """

    softwarelist = Software.objects.all().order_by('-total_number_of_downloads')

    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=softwarelist,
                                   template_name='software/software_list.html',
                                   )

def software_by_rating(request):
    """
    List of Software ranked by rating
    """
    # this may be omitted if we do these updates on any rating change
    # may lead to major speedups if we have many sw projects/ratings
    for s in Software.objects.all():
        s.average_rating = s.get_overall_rating()
        s.save(auto_update_date=False)

    softwarelist = Software.objects.all().order_by('-average_rating','-pub_date')

    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=softwarelist,
                                   template_name='software/software_list.html',
                                   )

def search_description(request, q):
    qs=Software.objects.get_by_searchterm(q)
    if qs.count()==0:
        return render_to_response('software/software_list.html',
                              { 'search_term': q, },
                                context_instance=RequestContext(request))
    else:
        return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=qs,
                                   template_name='software/software_list.html',
                                   extra_context={ 'search_term': q },
                                   )

