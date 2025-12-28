from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
import bcrypt
from django.conf import settings
from datetime import datetime, timedelta
from .models import User, AccessRoleRule
from .serializers import UserSerializer, AccessRoleRuleSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email, is_active=True)
            if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                payload = {
                    'user_id': user.id,
                    'exp': datetime.utcnow() + timedelta(hours=1)
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                return Response({'token': token})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        return Response({'message': 'Logged out'})

class UpdateProfileView(APIView):
    def put(self, request):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated'})
        return Response(serializer.errors, status=400)

class DeleteAccountView(APIView):
    def delete(self, request):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        user = request.user
        user.is_active = False
        user.save()
        return Response({'message': 'Account deleted (soft)'})

class AdminRulesView(APIView):
    def get(self, request):
        if not request.user or (request.user.role and request.user.role.name != 'admin'):
            return Response({'error': 'Forbidden'}, status=403)
        rules = AccessRoleRule.objects.all()
        serializer = AccessRoleRuleSerializer(rules, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user or (request.user.role and request.user.role.name != 'admin'):
            return Response({'error': 'Forbidden'}, status=403)
        serializer = AccessRoleRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk=None):
        if not request.user or (request.user.role and request.user.role.name != 'admin'):
            return Response({'error': 'Forbidden'}, status=403)
        try:
            rule = AccessRoleRule.objects.get(pk=pk)
            serializer = AccessRoleRuleSerializer(rule, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except AccessRoleRule.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)

    def delete(self, request, pk=None):
        if not request.user or (request.user.role and request.user.role.name != 'admin'):
            return Response({'error': 'Forbidden'}, status=403)
        try:
            rule = AccessRoleRule.objects.get(pk=pk)
            rule.delete()
            return Response({'message': 'Deleted'})
        except AccessRoleRule.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)

class MockProductsView(APIView):
    def get(self, request):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        rule = AccessRoleRule.objects.filter(role=request.user.role, element__name='products').first()
        if not rule or (not rule.read_permission and not rule.read_all_permission):
            return Response({'error': 'Forbidden'}, status=403)
        products = [{'id': 1, 'name': 'Product1', 'owner_id': request.user.id}, {'id': 2, 'name': 'Product2', 'owner_id': 999}]
        if rule.read_all_permission:
            return Response(products)
        else:
            return Response([p for p in products if p['owner_id'] == request.user.id])

    def post(self, request):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        rule = AccessRoleRule.objects.filter(role=request.user.role, element__name='products').first()
        if not rule or not rule.create_permission:
            return Response({'error': 'Forbidden'}, status=403)
        return Response({'message': 'Product created'})
    