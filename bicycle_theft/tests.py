from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory

from . import models 
from . import serializers
from . import views 


# class ViewResponseTest(APITestCase): 

#     def test_object_creation(self): 
#         self.test_obj = BicycleParkingFactory()

#         self.assertEqual(self.test_obj.__unicode__(), self.test_obj.gid)
#         self.assertEqual(self.test_obj.bilinear_score, 0.8812073629861754)
#         self.assertTrue(isinstance(self.test_obj, models.BicycleParkingPdx))

#     def test_view_returns_json_response(self):
#         self.test_obj = BicycleParkingFactory()
#         self.test_obj.save()
#         self.client = APIClient()

#         url = reverse('theft_app:rack_list')
#         self.assertEqual(url, '/api/v1/racks/'.decode('utf-8'))

#         resp = self.client.get(url)
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(resp.content, '{}') 

# class UrlParamsTest(APITestCase):

#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.client = APIClient()

#     def tearDown(self):
#         pass
    
#     def test_get_user_lat_long(self):
#         self.client = APIClient()
#         url = reverse('theft_app:rack_list')
#         self.assertEqual(url, '/api/v1/racks/')

#         resp = self.client.get(url)

#         self.assertEqual(resp.status_code, 200)

#     def test_get_user_dist_lat_long(self): 
#         pass

class TestAPIResponse(APITestCase):

    def setUp(self):
        models.BicycleParkingPdx.objects.create(gid = 10,
            degx = -122.656744,
            degy = 45.521292,
            geom = '01010000E0E610000076C7CD1808AA5EC06D3400AFB9C2464000000000000000000000000000000000',
            bilinear_score = 0.8812073629861754)


    def test_object_creation(self):
        test = models.BicycleParkingPdx.get(gid=10)

        self.assertEqual(test['degx'], -122.656744)



        





        
        
        








