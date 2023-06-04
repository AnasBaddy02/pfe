from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .models import Section, Discussion, Reply
from .forms import CreateSection, EditSection
from datetime import date



# Create your views here.
def plearn(request, id):
    if request.method == 'POST':
        if request.POST.get('addMessageForm'):
            discussion = Discussion.objects.create(
                message=request.POST["message"],
                date=date.today(),
                learner=request.user,
                section=Section.objects.get(id=id)
            )
            discussion.save()
        elif request.POST.get('addReplyForm'):
            reply = Reply.objects.create(
                response=request.POST["replyTextArea"+request.POST["addReplyForm"]],
                date=date.today(),
                editor = request.user,
                discussion = Discussion.objects.get(id = request.POST["addReplyForm"])
            )
            reply.save()
        
        return redirect('index', id=id)
    else:
        exists = Section.objects.filter(id=id).count()
        if exists == 1:
            current = Section.objects.get(id=id)
            sections = Section.objects.all().values()
            discussions = Discussion.objects.filter(section=id)
            replies = Reply.objects.filter(discussion__in=discussions)
            context = {
                'sections': sections,
                'current': current,
                'discussions': discussions,
                'replies': replies
            }
            return render(request ,'index.html', context)
    return render(request, '404.html')

def auth(request):
    not_valid = False
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user and user.is_active and not user.is_superuser:
            login(request, user)
            # Redirect to a success page.
            return redirect('index', id=Section.objects.all().first().id)
        else:
            not_valid = True
            return render(request, 'auth.html', {'not_valid': not_valid})
    else:
        return render(request, 'auth.html', {'not_valid': not_valid})

def register(request):
    exists = 0
    if request.method == "POST":
        exists = User.objects.filter(username=request.POST["username"]).count()
        if exists < 1:
            user = User.objects.create_user(username=request.POST["username"], email=request.POST["email"], password=request.POST["password1"])
            learners = Group.objects.get(name='learners')
            learners.user_set.add(user)
            return redirect('signin')
        
    return render(request ,'register.html', {'exists':exists})

def dashboard(request):
    if request.user and request.user.is_active and not request.user.is_superuser:
        if request.user.groups.all().first().name == 'editors':
            sections = Section.objects.all()
            context = {
                'sections': sections,
            }
            return render(request , 'dashboard.html', context)
    return render(request, '404.html')

def logout_user(request):
    logout(request)
    return redirect('index', id=Section.objects.all().first().id)

def create_section(request):
    if request.user and request.user.is_active and not request.user.is_superuser and request.user.groups.all().first().name == 'editors':
        if request.method == "POST":
            form = CreateSection(request.POST)
            notValid = False
            if form.is_valid():
                section = Section()
                section.name = request.POST.get('name')
                section.content = request.POST.get('content')
                section.video = request.POST.get('video') 
                section.save()
                return redirect('dashboard')
            else:
                form = CreateSection()
                notValid = True
                sections = Section.objects.all().values()
                context = {
                    'not_valid': notValid,
                    'sections': sections,
                    'form' : form
                }
                return render(request, 'create_section.html', context)
        else:
            form = CreateSection()
            sections = Section.objects.all().values()
            context = {
                'sections': sections,
                'form' : form
            }
            return render(request, 'create_section.html', context)
    
    return render(request, '404.html')

def edit_section(request, id):
    if request.user and request.user.is_active and not request.user.is_superuser and request.user.groups.all().first().name == 'editors':
        if request.method == "POST":
            if request.POST.get('editButton'):
                form = EditSection(request.POST)
                notValid = False
                if form.is_valid():
                    Section.objects.filter(id = id).update(
                        name=request.POST.get('name'),
                        content=request.POST.get('content'),
                        video=request.POST.get('video')
                    )
                else:
                    notValid = True
                    section = Section.objects.get(id=id)
                    form = EditSection(initial={
                        'name': section.name,
                        'content': section.content,
                        'video': section.video,
                    })
                    sections = Section.objects.all().values()
                    context = {
                        'sections': sections,
                        'form' : form,
                        'not_valid': notValid
                    }
                    return render(request, 'edit_section.html', context)
            elif request.POST.get('deleteButton'):
                Section.objects.filter(id = id).delete()

            return redirect('dashboard')
        else:
            exists = Section.objects.filter(id = id).count()
            if exists == 1:
                section = Section.objects.get(id=id)
                form = EditSection(initial={
                    'name': section.name,
                    'content': section.content,
                    'video': section.video,
                })
                sections = Section.objects.all().values()
                notValid = False
                context = {
                    'sections': sections,
                    'form' : form,
                    'not_valid': notValid
                }
                return render(request, 'edit_section.html', context)
    return render(request, '404.html')

def discussions(request, id):
    if request.user.groups.all().first().name == 'editors':
        if request.method == "POST":
            if request.POST.get("addReplyButton"):
                reply = Reply.objects.create(
                    response=request.POST.get("reply"+request.POST["addReplyButton"]),
                    date=date.today(),
                    editor = request.user,
                    discussion = Discussion.objects.get(id = request.POST["addReplyButton"])
                )
                reply.save()
            elif request.POST.get("deleteDiscussionButton"):
                Discussion.objects.filter(id = request.POST.get("deleteDiscussionButton")).delete()

        sectionDisc = Discussion.objects.filter(section = Section.objects.filter(id = id).first())
        sections = Section.objects.all().values()
        user = request.user
        sectionName = Section.objects.filter(id = id).first().name
        context = {
            'discussions': sectionDisc,
            'sections': sections,
            'sectionId': id,
            'sectionName': sectionName,
            'user': user
        }
        return render(request, 'discussions.html', context)
    return render(request, '404.html')

def replies(request, secId):
    if request.user.groups.all().first().name == 'editors':
        if request.method == "POST":
            if request.POST.get("deleteReplyButton"):
                Reply.objects.filter(id = request.POST.get("deleteReplyButton")).delete()
            elif request.POST.get("editReplyButton"):
                Reply.objects.filter(id = request.POST.get("editReplyButton")).update(
                    response = request.POST.get("reply"+request.POST.get("editReplyButton"))
                )
        discussions = Discussion.objects.filter(section = Section.objects.filter(id = secId).first())
        replies_list = Reply.objects.filter(discussion__in = discussions, editor = request.user)
        sections = Section.objects.all().values()
        secName = Section.objects.filter(id = secId).first().name
        context = {
            'replies': replies_list,
            'sections': sections,
            'sectionId': secId,
            'sectionName': secName
        }
        return render(request, 'replies.html', context)
    return render(request, '404.html')



def redirectToPlearn(request):
    return redirect('index', id=Section.objects.all().first().id)