from django.db import models
from mongoengine import *
from authentication.models import User
from io import BytesIO

class Cloth(DynamicDocument):
    id_ = IntField()
    owner = ReferenceField(User, required=True)
    usage_count = IntField(default=0)
    brand = StringField(max_length=50)
    category = StringField(max_length=50)
    size = StringField(max_length=50)
    image = FileField()
    color = StringField(max_length=50)
    

class ClothesManager:
    
    #TODO: distributed incremental id
    @classmethod
    def get_incremental_id(cls):
        return len(Cloth.objects.all())
    
    @classmethod
    def get_cloth_by_id(cls,id_):
        clothes = Cloth.objects.filter(id_=id_)
        print(len(clothes))
        return clothes[0] if len(clothes) > 0  else None
    
    @classmethod
    def cloth2json(cls, cloth):
        imageFile = cloth.image.read()
        return {
            'id_': cloth.id_,
            'owner': cloth.owner.username,
            'usage_count': cloth.usage_count,
            'brand': cloth.brand,
            'category': cloth.category,
            'size': cloth.size,
            'color':cloth.color,
            'image':bytes.decode(imageFile,encoding='utf-8') if imageFile != None else None
        }
    
    @classmethod
    def save_clothes(cls, clothes, username):
        print("username:", username)
        print("clothes:", clothes)
        print(type(clothes))
        if not isinstance(clothes, dict):
            response = {
                'status': '104',
                'message': 'Invalid clothes',
            }
        else:
            #1. save the clothes in MongoDB
            #2. count how many clothes are successfully saved
            #3. respond with the information of successfully saved data
            owner = User.get_user(username)
            clothes = [clothes]
            saved_clothes = []
            unsaved_clothes = []
            for cloth in clothes:
                #the user is only allowed to save his/her own clothes
                if cloth.get('owner') == username:
                    cloth_ = Cloth(owner = owner)
                    #TODO: extract and save more information
                    if 'usage_count' in cloth:
                        cloth_.usage_count = cloth['usage_count']
                    if 'brand' in cloth:
                        cloth_.brand = cloth['brand']
                    if 'category' in cloth:
                        cloth_.category = cloth['category']
                    if 'size' in cloth:
                        cloth_.size = cloth['size']
                    if 'color' in cloth:
                        cloth_.color = cloth['color']
                    if 'image' in cloth:
                        image_file = BytesIO(bytes(cloth['image'], encoding='utf-8'))
                        cloth_.image.put(image_file)
                    cloth_.id_ = ClothesManager.get_incremental_id()
                    print("save status:", cloth_.save())
                    print("cloth:", cloth_)
                    saved_clothes.append(ClothesManager.cloth2json(cloth_))
                else:
                    unsaved_clothes.append(cloth)
            response = {
                'status': '000',
                'message': 'Saved sucessfully',
                'data':{
                    'num': len(saved_clothes),
                    'saved_clothes': saved_clothes,
                    'unsaved_clothes': unsaved_clothes,
                }
            }
        return response
    
    @classmethod
    def get_clothes(cls, filters):
        #Pattern: filters
        print(filters['owner'])
        filters['owner'] = User.get_user(filters['owner'])
        #TODO: Range as a query option.
        
        clothes = Cloth.objects.filter(**filters)
        print(clothes)
        clothes = [] if clothes == None else [ClothesManager.cloth2json(cloth) for cloth in clothes]
        response = {
            'status': '000',
            'message': 'Query made successfully',
            'data':{
                'num': len(clothes),
                'clothes': clothes,
            }
        }
        return response