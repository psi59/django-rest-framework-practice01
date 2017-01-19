from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.decorators import api_view

from .models import User
from .models import Board
from .serializers import UserSerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# 회원가입
@api_view(['GET', 'POST'])
def sign_up(request):
    if request.method == 'POST':
        data = request.data
        if signup_validator(data) == status.HTTP_200_OK:
            user = User(name=data.get('name'), email=data.get('email'), password=data.get('password'))
            print(user)
            user.save()
            return JSONResponse('성공?')
    return JSONResponse('데이타 맨')


# 로그인
@api_view(['GET', 'POST'])
def sign_in(request):
    if 'user_id' in request.session:
        return redirect('detail')
    else:
        if request.method == "POST":
            data = request.data
            try:
                user = User.objects.get(email=data.get('email'))
                if user and user.password == data.get('password'):
                    request.session['user_id'] = user.id
                    return redirect('detail')
                else:   # 비밀번호 불일치시
                    return JSONResponse("잘못된 값")
            except User.DoesNotExist:
                return HttpResponse("존재하지 않는 유저")
        else:
            return render(request, 'signin.html')


# 회원수정
@api_view(['GET', 'POST'])
def update(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            data = request.data
            user = User.objects.get(pk=request.session['user_id'])
            user.name = data.get('name')
            user.password = data.get('password')
            user.email = data.get('email')
            user.save()
            request.session['user_id'] = user.id
            return redirect('detail')
    else:
        return JSONResponse("잘못된 값")


# 회원 상세정보
def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect("sign_in")


@csrf_exempt
def detail(request):
    user = User.objects.get(pk=request.session['user_id'])
    serializer = UserSerializer(user)
    return JSONResponse(serializer.data)


def signup_validator(data):
    if ('name' in data) and ('email' in data) and ('password' in data):
        if (User.objects.filter(email=data.get('email'))).exists():
            return status.HTTP_503_SERVICE_UNAVAILABLE
        return status.HTTP_200_OK
    return status.HTTP_400_BAD_REQUEST
