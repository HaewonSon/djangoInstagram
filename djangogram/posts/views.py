from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from djangogram.users.models import User as user_model
from django.urls import reverse

from . import models, serializers
from .forms import CreatePostForm, UpdatePostForm, CommentForm

# Create your views here.

def index(request): # 피드 페이지
    if request.method == 'GET':
        if request.user.is_authenticated:
            comment_form = CommentForm()

            user=get_object_or_404(user_model, pk=request.user.id)
            following=user.following.all()
            posts=models.Post.objects.filter(
                Q(author__in=following) | Q(author=user)
            ).order_by("-create_at") # 피드 데이터 표출 순서
            serializer = serializers.PostSerializer(posts, many=True)
            print(serializer.data)

            return render(
                request,
                'posts/main.html',
                {"posts":serializer.data, "comment_form":comment_form}
            )



def post_create(request):
    if request.method == 'GET':
        # 사용자가 페이지 요청할 때
        form = CreatePostForm()
        return render(request, 'posts/post_create.html',{"form":form})

    elif request.method == 'POST':
        if request.user.is_authenticated: # 로그인 되어있을때만 포스트 작성 가능

            user = get_object_or_404(user_model, pk=request.user.id)
            # image = request.FILES['image'] # 파일 데이터
            # caption = request.POST['caption'] # 파일 외의 데이터
            #
            # new_post = models.Post.objects.create(
            #     author = user,
            #     image = image,
            #     caption = caption
            # )
            # new_post.save() # 포스트 객체 저장

            form = CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = user
                post.save()
            else:
                print(form.errors)

            return render(request, 'posts/main.html') # 피드 페이지로 돌아감

        else: # 로그인이 안되어있으면 유저 메인 페이지로 이동
            return render(request, 'users/main.html')

def post_update(request, post_id):
    if request.user.is_authenticated:
        # 작성자 체크
        post = get_object_or_404(models.Post, pk=post_id)
        if request.user != post.author:
            return redirect(reverse('posts:index'))

        # GET 요청
        if request.method == 'GET':
            form  = UpdatePostForm(instance=post)
            return render(
                request,
                'posts/post_update.html',
                {"form":form, "post":post}
            )

        elif request.method == 'POST':
            # 업데이트 버튼 클릭 후 저장을 위한 POST api 요청 로직
            form = UpdatePostForm(request.POST)
            if form.is_valid():
                post.caption = form.cleaned_data['caption']
                post.save()

            return redirect(reverse('posts:index'))


    else :
        return render(request,'users/main.html')


def post_delete(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(models.Post, pk=post_id) # 게시물이 존재하는지 확인
        if request.user == post.author:  # 현재 로그인 유저가 게시 작성자인지 확인
            post.delete()
        return redirect(reverse('posts:index'))

    else:
        return render(request, 'users/main.html')


def comment_create(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(models.Post, pk=post_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.posts = post
            comment.post_id = post.pk # 이 한줄로 이틀을 보내다니 ㅜㅡㅜ
            comment.save()


            return redirect(reverse('posts:index') + "#comment-"+ str(comment.id))

        else:
            return render(request, 'users/main.html')


def comment_delete(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(models.Comment, pk=comment_id) # 댓글이 존재하는지 확인
        if request.user == comment.author: # 현재 로그인 유저가 댓글의 작성자인지 확인
            comment.delete()
        return redirect(reverse('posts:index'))

    else:
        return render(request, 'users/main.html')
