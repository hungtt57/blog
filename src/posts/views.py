try:
	from urllib.parse import quote_plus #python 3
except:
	pass
	
from urllib import quote_plus
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage , PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render , get_object_or_404 , redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.db.models import Q
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from .utils import get_read_time
# Create your views here.
def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	form = PostForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request,'Successfully Created')
		return HttpResponseRedirect(instance.get_absolute_url())
	# if request.method == "POST":
	# 	print request.POST.get("content")
	# 	print request.POST.get("title")
		# Post.objects.create(title=title)

	context = {
		"form" : form,
	}
	return render(request,"post_form.html",context)

def post_detail(request,slug=None):
	# instance = Post.object.get(id=1)
	instance = get_object_or_404(Post,slug=slug)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)
	
	initial_data = {
		"content_type":instance.get_content_type,
		"object_id" : instance.id
	}
	form = CommentForm(request.POST or None,initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type= form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get('content')
		parent_obj=None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() ==1 :
				parent_obj = parent_qs.first()	
		new_comment,created = Comment.objects.get_or_create(
												user=request.user,
												content_type=content_type,
												object_id = obj_id,
												content = content_data,
												parent = parent_obj
												)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"instance": instance,
		"share_string":share_string,
		"comments": comments,
		"comment_form" : form
	}
	return render(request,"post_detail.html",context)

def post_list(request):
	today = timezone.now().date()
	queryset_list= Post.objects.active()#order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()



	paginator = Paginator(queryset_list,2)
	page_request_get = 'page'
	page = request.GET.get(page_request_get)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page is not an integer.deliver first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of range,deliver last page of results
		queryset = paginator.page(paginator.num_pages)




	context = {
		"object_list":queryset,
		"title":"list",
		"page_request_get":page_request_get,
		"today":today
	}
	# if request.user.is_authenticated():
	# 	context = {
	# 		"title":"My user list"
	# 	}
		
	# else:
	# 	context = {
	# 	"title":"list"
	# 	}
	return render(request,"post_list.html",context)

def post_update(request,slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post,slug=slug)
	form = PostForm(request.POST or None,request.FILES or None,instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		# message success
		messages.success(request,'<a href="#">Item </a> Saved',extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"title": instance.title,
		"instance": instance,
		"form" : form
	}
	return render(request,"post_form.html",context)

def post_delete(request,slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post,slug=slug)
	instance.delete()
	messages.success(request,"Successfully deleted")
	return redirect("posts:list")