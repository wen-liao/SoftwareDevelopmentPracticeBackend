from django.http import JsonResponse
from clothes_management.models import Cloth, ClothesManager
from authentication.models import User

import json

# Create your views here.

def get_body(request):
    try:
        body = json.loads(bytes.decode(request.body, encoding='utf-8'))
        print(body)
    except:
        return None
    else:
        return body

def upload_clothes(request):
    if request.method == 'POST':
        body = get_body(request)
        if (body == None) or (not isinstance(body, dict)) :
            response = {
                'status': '101',
                'message': 'Ill-formed JSON body',
            }
        else:
            username = body.get('username')
            if username == None:
                response = {
                    'status': '102',
                    'message': 'Username missing',
                }
            #elif username != request.session.get('username'):
            #    response = {
            #        'status': '103',
            #        'message': 'Not logged in',
            #    }
            else:
                clothes = body.get('clothes')
                response = ClothesManager.save_clothes(clothes, username)
    else:
        response = {
            'status': '100',
            'message': 'Fail to upload',
        }
    print(response)
    return JsonResponse(response)
    
def get_clothes(request):
    if request.method == 'POST':
        body = get_body(request)
        if (body == None) or (not isinstance(body, dict)):
            response = {
                'status': '101',
                'message': 'Ill-formed JSON body'
            }
        else:
            owner = body.get('owner')
            print(request.session.items())
            print(request.COOKIES)
            if owner == None:
                response = {
                    'status': '102',
                    'message': 'Missing owner\'s name',
                }
                '''
                elif owner != request.session.get('username'):
                    response = {
                        'status': '103',
                        'message': 'Not logged in',
                    }
                '''
            else:
                #Pattern: filters
                filters = body
                if 'image' in body:
                    del(body['image'])
                response = ClothesManager.get_clothes(filters)
    else:
        response = {
            'status': '100',
            'message': 'Fail to get information on clothes.',
        }
    print(response)
    return JsonResponse(response)