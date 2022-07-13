from django.shortcuts import render,HttpResponse
import queue
from django.http import JsonResponse


# Create your views here.

USER_QUEUE = { }


def home(request):
    uid = request.GET.get('uid')
    USER_QUEUE[uid] = queue.Queue()

    return render(request,'home.html',{"uid":uid})


def send_msg(request):
    text = request.GET.get('text')
    for uid,q in USER_QUEUE.items():
        q.put(text)

    return HttpResponse("OK")


def get_msg(request):
    # 去自己的队列中获取数据，uid
    uid = request.GET.get('uid')
    q = USER_QUEUE[uid]

    result = {'status':True, 'data':None}

    try:
        data = q.get(timeout=10)
        result["data"] = data
    except queue.Empty as e:
        result["status"] = False
    return JsonResponse(result)


