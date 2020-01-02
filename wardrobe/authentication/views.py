from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from authentication.models import * #User

import json

# Create your views here.

def register(request):
    if request.method == 'POST':
        try:
            body = json.loads(bytes.decode(request.body, encoding='utf-8'))
            print(body)
        except:
            response = {
                'status': '101',
                'message': 'Ill-formed JSON request body'
            }
        else:
            username, email, password = body.get('username'), body.get('email'), body.get('password')
            if username == None or email == None or password == None:
                response = {
                    'status': '102',
                    'message': 'Missing user fields',
                }
            else:
                user = User.get_user(username)
                if user != None:
                    response = {
                        'status': '103',
                        'message': 'User already exists',
                    }
                else:
                    encrypted_password = make_password(password, None, 'pbkdf2_sha256')
                    user = {
                        'username':username,
                        'email':email,
                        'encrypted_password':encrypted_password,
                    }
                    User.register(user)
                    response = {
                        'status':'000',
                        'message': 'Registered successfully',
                    }

    else:
        response = {
            'status': '100',
            'message': 'Fail to register',
        }
    print(response)
    return JsonResponse(response)

def sign_in(request):
    if request.method == 'POST':
        try:
            body = json.loads(bytes.decode(request.body, encoding='utf-8'))
            print(body)
        except:
            response = {
                'status': '101',
                'message': 'Ill-formed JSON request body'
            }
        else:
            username, password = body.get('username'), body.get('password')
            if username == None:
                response = {
                    'status': '102',
                    'message': 'Missing username',
                }
            else:
                user = User.get_user(username)
                '''
                if user == None:
                    response = {
                        'status': '103',
                        'message': 'User does not exist',
                    }
                elif password == None:
                    response = {
                        'status': '104',
                        'message': 'Missing password',
                    }
                elif check_password(password, user.encrypted_password) == False:
                    response = {
                        'status': '105',
                        'message': 'Wrong password',
                    }
                elif 'username' not in request.session:
                    request.session['username'] = username
                    print("Session items:", request.session.items())
                    print(request.COOKIES)
                    response = {
                        'status': '000',
                        'message': 'Signed in successfully',
                    }
                else:
                    response = {
                        'status': '001',
                        'message': 'Signed in already',
                    }
                '''
                response = {
                        'status': '000',
                        'message': 'Signed in successfully',
                    }
    else:
        response = {
            'status': '100',
            'message': 'Fail to log in',
        }
    print("response:", response)
    return JsonResponse(response)


def sign_out(request):
    if request.method == 'POST':
        try:
            body = json.loads(bytes.decode(request.body, encoding='utf-8'))
            print(body)
        except:
            response = {
                'status': '101',
                'message': 'Ill-formed JSON request body'
            }
        else:
            response = {
                    'status': '000',
                    'message': 'Signed out successfully',
                }
            '''username = body.get('username')
            if request.session.get('username') == username:
                print(request.COOKIES)
                del(request.session['username'])
                response = {
                    'status': '000',
                    'message': 'Signed out successfully',
                }
            else:
                response = {
                    'status': '102',
                    'message': 'Not logged in',
                }
               '''
    else:
        response = {
            'status': '100',
            'message': 'Fail to log out'
        }
    print(response)
    return JsonResponse(response)