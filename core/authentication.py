from django.contrib.auth.hashers import check_password
import jwt
from rest_framework.response import Response
from rest_framework import status


secret = "secret_key"
def encode_token(email, password, model):
    if not email and password:
        return Response({"Email/ Password is required"},status=status.HTTP_400_BAD_REQUEST)
    try:
        user = model.objects.get(email=email)
        user_id = user.id 
        if check_password(password,user.password):
            encoded = jwt.encode({"email":email, "id":user_id}, secret, algorithm="HS256")
            print(encoded,"token")
            return Response({"token":encoded},status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"Email/ Password does not match"},status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"error":"user does not exist"},status=status.HTTP_400_BAD_REQUEST)



def decode_token(request,model,serializer):
    token = request.headers.get('Authorization')
    if not token:
        return Response({"error":"Token is required"},status=status.HTTP_400_BAD_REQUEST)
    try:
        decoded = jwt.decode(token, secret, algorithms="HS256")
        user_id = decoded.get('id')
        # print(user_id)
        queryset = model.objects.filter(id=user_id).first()

        if not queryset:
            return Response({"error":"Enter valid token"},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = serializer(queryset) 
        return Response(serializer.data, status=status.HTTP_200_OK) 
    except Exception as e:
        print("token change")
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    