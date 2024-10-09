from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from inventory_management import ins_logger
from item.models import item
from django.core.cache import cache


class itemMaster(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            if request.data.get('vchr_name') and request.data.get('txt_description'):
                # Check if item with the same name already exists
                if item.objects.filter(vchr_name=request.data.get('vchr_name')).exists():
                    return Response({'status': 0, 'reason': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

                item.objects.create(
                    vchr_name=request.data.get('vchr_name'),
                    txt_description=request.data.get('txt_description'),
                    int_status=1
                )
                cache.delete('active_items_list') 
                return Response({'status': 1, "message": "Item created successfully"}, status=status.HTTP_201_CREATED)
            
            return Response({'status': 0, 'reason': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id), 'details': 'line no: ' + str(e.__traceback__.tb_lineno)})
            return Response({'status': 0, 'reason': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, item_id=None):
        try:
            
            cache_key = 'active_items_list'  # Define a cache key for the item list
            
            lst_item = cache.get(cache_key)
            
            if lst_item is None:
                # If not found in cache, fetch from the database
                lst_item = item.objects.filter(int_status=1).values('vchr_name', 'txt_description')
                # Cache the result for 5 minutes (300 seconds)
                cache.set(cache_key, lst_item, timeout=300)
            
            # lst_item = item.objects.filter(int_status=1).values('vchr_name', 'txt_description')
            return Response({"status": 1, "data": lst_item}, status=status.HTTP_200_OK)
        
        except Exception as e:
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id), 'details': 'line no: ' + str(e.__traceback__.tb_lineno)})
            return Response({'status': 0, 'reason': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, item_id):
        try:
            obj_item = item.objects.get(id=item_id)

            # Ensure the new name does not conflict with existing items (except itself)
            if item.objects.filter(vchr_name=request.data.get('vchr_name')).exclude(id=item_id).exists():
                raise Exception('Item name already exists.')

            obj_item.vchr_name = request.data.get('vchr_name', obj_item.vchr_name)
            obj_item.txt_description = request.data.get('txt_description', obj_item.txt_description)
            obj_item.save()
            cache.delete('active_items_list') 
            return Response({"status": 1, "message": "Item updated successfully"}, status=status.HTTP_200_OK)
        
        except item.DoesNotExist:
            return Response({"status": 0, "message": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id), 'details': 'line no: ' + str(e.__traceback__.tb_lineno)})
            return Response({'status': 0, 'reason': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, item_id):
        try:
            obj_item = item.objects.get(id=item_id)
            obj_item.int_status = 0  # Mark item as inactive
            obj_item.save()
            cache.delete('active_items_list') 
            return Response({"status": 1, "message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
        except item.DoesNotExist:
            return Response({"status": 0, "message": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id), 'details': 'line no: ' + str(e.__traceback__.tb_lineno)})
            return Response({'status': 0, 'reason': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
