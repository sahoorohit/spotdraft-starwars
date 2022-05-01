import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from planets.models import Planet


class PlanetListTest(APITestCase):

    @property
    def url(self) -> str:
        return reverse('planets_list')

    def test_create_planet_when_name_missing_in_payload__failure(self):
        response = self.client.post(self.url, data={"name": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['name'][0], 'This field may not be blank.')

    def test_create_planet_when_is_favorite_missing_in_payload__success(self):
        planet_name = "Planet 1"
        response = self.client.post(self.url, data={"name": planet_name})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], "Planet created successfully.")
        self.assertEqual(response_body['details']['name'], planet_name)
        self.assertFalse(response_body['details']['is_favorite'])
        self.assertIsNotNone(response_body['details']['created_at'])
        self.assertIsNotNone(response_body['details']['updated_at'])

        planet = Planet.objects.get(name=planet_name)
        self.assertFalse(planet.is_favorite)

    def test_create_planet_when_is_favorite_specified_in_payload__success(self):
        planet_name = "Planet 1"
        response = self.client.post(self.url, data={"name": planet_name, "is_favorite": True})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], "Planet created successfully.")
        self.assertEqual(response_body['details']['name'], planet_name)
        self.assertTrue(response_body['details']['is_favorite'])
        self.assertIsNotNone(response_body['details']['created_at'])
        self.assertIsNotNone(response_body['details']['updated_at'])

        planet = Planet.objects.get(name=planet_name)
        self.assertTrue(planet.is_favorite)

    def test_get_planet_list_when_no_planet_exists__success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], 'Empty planet list.')
        self.assertEqual(len(response_body['planets']), 0)

    def test_get_planet_list_when_planet_exists__success(self):
        self.test_create_planet_when_is_favorite_specified_in_payload__success()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], 'Planet list fetched successfully.')
        self.assertEqual(len(response_body['planets']), 1)

        first_planet = response_body['planets'][0]
        self.assertEqual(first_planet['name'], "Planet 1")
        self.assertTrue(first_planet['is_favorite'])
        self.assertIsNotNone(first_planet['created_at'])
        self.assertIsNotNone(first_planet['updated_at'])
        self.assertIsNotNone(first_planet['url'])
        self.assertTrue(first_planet['url'].endswith(reverse("planet_detail", args=(1,))))

    def test_get_planet_list_when_no_planet_exists_by_name__success(self):
        response = self.client.get(f'{self.url}?name=invalid-name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], 'Empty planet list.')
        self.assertEqual(len(response_body['planets']), 0)

    def test_get_planet_list_when_planet_exists_by_name__success(self):
        Planet.objects.create(name="Coruscant")
        Planet.objects.create(name="Alderaanta")
        Planet.objects.create(name="Hoth")

        planets = Planet.objects.all()
        self.assertEqual(len(planets), 3)

        response = self.client.get(f'{self.url}?name=ant')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], 'Planet list fetched successfully.')
        self.assertEqual(len(response_body['planets']), 2)

        first_planet = response_body['planets'][0]
        self.assertEqual(first_planet['name'], "Coruscant")
        self.assertFalse(first_planet['is_favorite'])
        self.assertIsNotNone(first_planet['created_at'])
        self.assertIsNotNone(first_planet['updated_at'])
        self.assertIsNotNone(first_planet['url'])
        self.assertTrue(first_planet['url'].endswith(reverse("planet_detail", args=(1,))))


class PlanetDetailTest(APITestCase):

    def url(self, id: int) -> str:
        return reverse('planet_detail', args=(id,))

    def test_get_movie_detail_when_id_is_invalid__failure(self):
        response = self.client.get(self.url(id=1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_movie_detail_when_id_is_valid__success(self):
        planet_name = "Planet 1"
        Planet.objects.create(name=planet_name)

        response = self.client.get(self.url(id=1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], "Planet details fetched successfully.")
        self.assertEqual(response_body['details']['name'], planet_name)
        self.assertFalse(response_body['details']['is_favorite'])
        self.assertIsNotNone(response_body['details']['created_at'])
        self.assertIsNotNone(response_body['details']['updated_at'])


class PlanetFavoriteTest(APITestCase):

    def url(self, id: int) -> str:
        return reverse('planet_favorite', args=(id, ))

    def test_add_favorite_planet_when_planet_id_is_invalid__failure(self):
        response = self.client.post(self.url(id=1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_favorite_planet_when_custom_name_is_not_in_payload__success(self):
        planet = Planet.objects.create(name="Coruscant")
        self.assertFalse(planet.is_favorite)
        self.assertIsNone(planet.custom_name)

        response = self.client.post(self.url(id=1))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        planet.refresh_from_db()
        self.assertTrue(planet.is_favorite)
        self.assertIsNone(planet.custom_name)

    def test_add_favorite_planet_when_custom_name_is_in_payload__success(self):
        planet = Planet.objects.create(name="Coruscant")
        self.assertFalse(planet.is_favorite)
        self.assertIsNone(planet.custom_name)

        custom_name = "new custom name"
        response = self.client.post(self.url(id=1), data={"custom_name": custom_name})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        planet.refresh_from_db()
        self.assertTrue(planet.is_favorite)
        self.assertEqual(planet.custom_name, custom_name)
