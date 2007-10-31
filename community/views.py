"""
All forum logic is kept here - displaying lists of forums, threads 
and posts, adding new threads, and adding replies.
"""

from community.models import Forum,Thread,Post
from datetime import datetime
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import newforms as forms
from django.contrib.auth import authenticate, login

class NewPostForm(forms.Form):
	body = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":80}))

class NewPostFormwPassword(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'size':'20'}), required=True, max_length=40)
	username = forms.CharField(widget=forms.TextInput(attrs={'size':'20'}), required=True, max_length=40)
	body = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":80}))

	def clean_username(self):
		if 'username' not in self.cleaned_data:
			raise forms.ValidationError(u'This field is required.')
		if 'username' in self.data and 'password' in self.data:
			username=self.cleaned_data['username']
			password=self.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					self.user = user
				else:
					raise forms.ValidationError(u'User Account disabled.')
			else:
				raise forms.ValidationError(u'Please enter a correct username and password. Note that both fields are case-sensitive.')

	def login(self, request):
		if self.is_valid():
			login(request, self.user)
			return request.user.is_authenticated()
		return False

def create_newpostform(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			inputform = NewPostForm(request.POST)
		else:
			inputform = NewPostForm()
	else:
		if request.method == 'POST':
			inputform = NewPostFormwPassword(request.POST)
		else:
			inputform = NewPostFormwPassword()
	return inputform

class NewThreadForm(forms.Form):
	body = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":80}))
	title = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=True, max_length=100)

class NewThreadFormwPassword(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'size':'20'}), required=True, max_length=40)
	username = forms.CharField(widget=forms.TextInput(attrs={'size':'20'}), required=True, max_length=40)
	title = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=True, max_length=100)
	body = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":80}))

	def clean_username(self):
		if 'username' not in self.cleaned_data:
			raise forms.ValidationError(u'This field is required.')
		if 'username' in self.data and 'password' in self.data:
			username=self.cleaned_data['username']
			password=self.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					self.user = user
				else:
					raise forms.ValidationError(u'User Account disabled.')
			else:
				raise forms.ValidationError(u'Please enter a correct username and password. Note that both fields are case-sensitive.')

	def login(self, request):
		if self.is_valid():
			login(request, self.user)
			return True
		return False

def create_newthreadform(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			inputform = NewThreadForm(request.POST)
		else:
			inputform = NewThreadForm()
	else:
		if request.method == 'POST':
			inputform = NewThreadFormwPassword(request.POST)
		else:
			inputform = NewThreadFormwPassword()
	return inputform


def forum(request, slug):
	"""
	Displays a list of threads within a forum.
	Threads are sorted by their sticky flag, followed by their 
	most recent post.
	"""
	f = get_object_or_404(Forum, slug=slug)

	inputform = create_newthreadform(request)

	return render_to_response('community/thread_list.html',
		RequestContext(request, {
			'forum': f,
			'form': inputform,
			'form_action' : 'new/',
			'threads': f.thread_set.all()
		}))

def thread(request, forum, thread):
	"""
	Increments the viewed count on a thread then displays the 
	posts for that thread, in chronological order.
	"""
	f = get_object_or_404(Forum, slug=forum)
	t = get_object_or_404(Thread, pk=thread)
	p = t.post_set.all().order_by('time')

	t.views += 1
	t.save()

	inputform = create_newpostform(request)
	
	return render_to_response('community/thread.html',
		RequestContext(request, {
			'forum': f,
			'form': inputform,
			'thread': t,
			'posts': p,
			'form_action' : 'reply/'
		}))

def newthread(request, forum):
	"""
	Rudimentary post function - this should probably use 
	newforms, although not sure how that goes when we're updating 
	two models.

	Only allows a user to post if they're logged in.
	"""
	f = get_object_or_404(Forum, slug=forum)
	t = f.thread_set.all().order_by('thread_latest_post')[:1]

	if request.method == 'POST':
		form = create_newthreadform(request)
		if form.is_valid():
			if request.user.is_authenticated() or form.login(request):
				t = Thread(
					forum=f,
					title=form.cleaned_data['title'],
				)
				t.save()
				p = Post(
					thread=t,
					author=request.user,
					body=form.cleaned_data['body'],
					time=datetime.now(),
				)
				p.save()
				return HttpResponseRedirect(t.get_absolute_url())
	else:
		form = create_newthreadform(request)
	
	return render_to_response('community/thread_list.html',
			RequestContext(request, {
			'forum': f,
			'form': form,
			'form_action' : '',
			'threads': t
			}))

def reply(request, forum, thread):
	"""
	If a thread isn't closed, and the user is logged in, post a reply
	to a thread. Note we don't have "nested" replies at this stage.
	"""
	f = get_object_or_404(Forum, slug=forum)
	t = get_object_or_404(Thread, pk=thread)
	p = t.post_set.all().order_by('-time')[:1]

	if t.closed:
		return HttpResponseRedirect('/accounts/login?next=%s' % request.path)

	if request.method == 'POST':
		form = create_newpostform(request)
		if form.is_valid():
			if request.user.is_authenticated() or form.login(request):
				p = Post(
					thread=t, 
					author=request.user,
					body=form.cleaned_data['body'],
					time=datetime.now(),
					)
				p.save()
				return HttpResponseRedirect(p.get_absolute_url())
	else:
		form = create_newpostform(request)

	return render_to_response('community/thread.html',
			RequestContext(request, {
			'forum': f,
			'thread': t,
			'posts': p,
			'form': form,
			'form_action' : ''
			}))

