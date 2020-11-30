from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import json

# Create your views here.
from virtual_queue.models import *


def host_home(request):
    user = request.user
    if not user.is_anonymous:
        if not Queue.objects.filter(user=user).exists():
            return redirect('/host/register')
        queue = Queue.objects.get(user=user)
        positions = QueuePosition.objects.filter(queue=queue)
        return render(request, 'host.html', {'queue': queue, 'positions': positions})
    return render(request, 'host.html')


def host_register(request):
    print('loloolol')
    if request.method == 'POST':
        print(request, request.POST)
        full_name = request.POST.get('full_name')
        first_name = str(full_name).split(' ')[0]
        last_name = str(full_name).split(' ')[-1]
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')

        queue_name = request.POST.get('queue_name')
        queue_info = request.POST.get('queue_info')
        queue_loc = request.POST.get('queue_loc')

        if User.objects.filter(email=email_id).exists():
            response = {'status': 1, 'message': 'Account already exists.', 'url': '/host/login'}
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            user = User(first_name=first_name, last_name=last_name, username=email_id,
                        email=email_id)
            user.set_password(password)
            user.save()
            queue = Queue(user=user, name=queue_name, details=queue_info, location=queue_loc)
            queue.save()

            response = {'status': 1, 'message': 'Account Created', 'url': '/host/login'}
            return HttpResponse(json.dumps(response), content_type='application/json')

    return render(request, 'host.html')


def host_login(request):
    if request.method == 'POST':
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')
        user = authenticate(username=email_id, password=password)

        if user is not None:
            login(request, user)
            # doctor = Doctor.objects.filter(user=user)[0]
            response = {'status': 1, 'message': 'Logged In Successfully', 'url': '/host'}
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            response = {'status': 2, 'message': 'Invalid Username or Password', 'url': '/host/login'}
            return HttpResponse(json.dumps(response), content_type='application/json')

    return render(request, 'host.html')


def join_home(request):
    user = request.user
    context = {}
    if not user.is_anonymous:
        if QueuePosition.objects.filter(user=user).exists():
            qp = QueuePosition.objects.get(user=user)
            context['qp'] = qp
        else:
            queues = Queue.objects.all()
            context['queues'] = queues
    return render(request, 'join.html', context=context)


def join_register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        first_name = str(full_name).split(' ')[0]
        last_name = str(full_name).split(' ')[-1]
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')

        if User.objects.filter(email=email_id).exists():
            response = {'status': 1, 'message': 'Account already exists.', 'url': '/join'}
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            user = User(first_name=first_name, last_name=last_name, username=email_id,
                        email=email_id)
            user.set_password(password)
            user.save()

            response = {'status': 1, 'message': 'Account Created', 'url': '/join'}
            return HttpResponse(json.dumps(response), content_type='application/json')

    return render(request, '')


def join_login(request):
    if request.method == 'POST':
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')
        user = authenticate(username=email_id, password=password)

        if user is not None:
            login(request, user)
            response = {'status': 1, 'message': 'Logged In Successfully', 'url': '/join'}
            print('logged in')
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            response = {'status': 2, 'message': 'Invalid Username or Password', 'url': '/join'}
            print('no user')
            return HttpResponse(json.dumps(response), content_type='application/json')

    return render(request, '')


def join_request(request):
    user = request.user
    if user.is_anonymous:
        return redirect('/join/login')
    qid = str(request.POST.get('queue_id')).split('join')[-1]
    queue = Queue.objects.get(pk=qid)

    count = QueuePosition.objects.filter(queue=queue).count()

    new_posi = QueuePosition(user=user, queue=queue, rank=count+1)
    new_posi.save()

    return HttpResponse('Entered')


def delete_request(request):
    if request.method == 'POST':
        p = request.POST.get('posi_id')
        posi = get_object_or_404(QueuePosition, pk=p)
        posi.delete()
        update_ranks(posi.queue)
    else:
        p = request.GET.get('posi_id')
        posi = get_object_or_404(QueuePosition, pk=p)
        posi.delete()
        update_ranks(posi.queue)

    return HttpResponse('Done')


def logout_request(request):
    logout(request)
    return redirect('/')


def update_ranks(q):
    queryset = QueuePosition.objects.filter(queue=q).order_by('timestamp')
    temp = 1
    for i in queryset:
        i.rank = temp
        temp += 1
        i.save()
