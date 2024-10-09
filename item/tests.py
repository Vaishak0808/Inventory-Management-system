from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from item.models import item

class ItemMasterTestCase(APITestCase):
    
    def setUp(self):
        # Create initial data for testing
        self.item1 = item.objects.create(vchr_name="Item 1", txt_description="Description 1", int_status=1)
        self.item2 = item.objects.create(vchr_name="Item 2", txt_description="Description 2", int_status=1)
        self.item_inactive = item.objects.create(vchr_name="Inactive Item", txt_description="Inactive", int_status=0)
        
        self.valid_data = {
            "vchr_name": "New Item",
            "txt_description": "New Description"
        }
        self.invalid_data = {
            "vchr_name": "",
            "txt_description": ""
        }

    def test_create_item_valid(self):
        # Test POST method with valid data
        response = self.client.post(reverse('item_list_create'), data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(item.objects.count(), 4)  # 3 items in setUp and 1 new item

    def test_create_item_missing_fields(self):
        # Test POST method with missing fields
        response = self.client.post(reverse('item_list_create'), data=self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_items_list(self):
        # Test GET method to retrieve active items
        response = self.client.get(reverse('item_list_create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)  # Only 2 active items should be returned

    def test_get_items_list_no_active(self):
        # Test GET method when there are no active items
        item.objects.filter(int_status=1).update(int_status=0)  # Set all items to inactive
        response = self.client.get(reverse('item_list_create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 0)  # No active items should be returned

    def test_update_item_valid(self):
        # Test PUT method with valid data
        update_data = {
            "vchr_name": "Updated Item 1",
            "txt_description": "Updated Description 1"
        }
        response = self.client.put(reverse('item_update_delete', kwargs={'item_id': self.item1.id}), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.vchr_name, "Updated Item 1")
        self.assertEqual(self.item1.txt_description, "Updated Description 1")

    def test_update_item_invalid_id(self):
        # Test PUT method with an invalid item ID
        update_data = {
            "vchr_name": "Nonexistent Item",
            "txt_description": "Nonexistent Description"
        }
        response = self.client.put(reverse('item_update_delete', kwargs={'item_id': 999}), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item_valid(self):
        response = self.client.delete(reverse('item_update_delete', kwargs={'item_id': self.item1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        item1 = item.objects.get(id=self.item1.id)
        self.assertEqual(item1.int_status, 0)
    def test_delete_item_invalid_id(self):
        # Test DELETE method with an invalid item ID
        response = self.client.delete(reverse('item_update_delete', kwargs={'item_id': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
