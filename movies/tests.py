import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from movies.models import Movie


class MovieListTest(APITestCase):

    @property
    def url(self) -> str:
        return reverse('movies_list')

    def test_create_movie_when_name_missing_in_payload__failure(self):
        response = self.client.post(self.url, data={"name": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['name'][0], 'This field may not be blank.')

    def test_create_movie_when_release_date_missing_in_payload__failure(self):
        response = self.client.post(self.url, data={"name": "Movie 1"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['release_date'][0], 'This field is required.')

    def test_create_movie_when_is_favorite_missing_in_payload__success(self):
        movie_name = "Movie 1"
        release_date = "2022-05-01"
        response = self.client.post(self.url, data={"name": movie_name, "release_date": release_date})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], "Movie created successfully.")
        self.assertEqual(response_body['details']['name'], movie_name)
        self.assertFalse(response_body['details']['is_favorite'])
        self.assertEqual(response_body['details']['release_date'], release_date)
        self.assertIsNotNone(response_body['details']['created_at'])
        self.assertIsNotNone(response_body['details']['updated_at'])

        movie = Movie.objects.get(name=movie_name)
        self.assertFalse(movie.is_favorite)
        self.assertEqual(str(movie.release_date), release_date)

    def test_create_movie_when_is_favorite_specified_in_payload__success(self):
        movie_name = "Movie 1"
        release_date = "2022-05-01"
        response = self.client.post(
            self.url,
            data={"name": movie_name, "release_date": release_date, "is_favorite": True}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], "Movie created successfully.")
        self.assertEqual(response_body['details']['name'], movie_name)
        self.assertTrue(response_body['details']['is_favorite'])
        self.assertEqual(response_body['details']['release_date'], release_date)
        self.assertIsNotNone(response_body['details']['created_at'])
        self.assertIsNotNone(response_body['details']['updated_at'])

        movie = Movie.objects.get(name=movie_name)
        self.assertTrue(movie.is_favorite)
        self.assertEqual(str(movie.release_date), release_date)

    def test_get_movie_list_when_no_movie_exists__success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], 'Empty Movie list.')
        self.assertEqual(len(response_body['movies']), 0)

    def test_get_movie_list_when_movie_exists__success(self):
        self.test_create_movie_when_is_favorite_specified_in_payload__success()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], 'Movie list fetched successfully.')
        self.assertEqual(len(response_body['movies']), 1)

        first_movie = response_body['movies'][0]
        self.assertEqual(first_movie['name'], "Movie 1")
        self.assertTrue(first_movie['is_favorite'])
        self.assertIsNotNone(first_movie['created_at'])
        self.assertIsNotNone(first_movie['updated_at'])
        self.assertIsNotNone(first_movie['url'])
        self.assertTrue(first_movie['url'].endswith(reverse("movie_detail", args=(1,))))

    def test_get_movie_list_when_no_movie_exists_by_name__success(self):
        response = self.client.get(f'{self.url}?name=invalid-name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], 'Empty Movie list.')
        self.assertEqual(len(response_body['movies']), 0)

    def test_get_movie_list_when_movie_exists_by_name__success(self):
        Movie.objects.create(name="A New Hope", release_date="2022-05-01")
        Movie.objects.create(name="Return of the Jedi", release_date="2022-05-01")
        Movie.objects.create(name="Revenge of the Sith", release_date="2022-05-01")

        movies = Movie.objects.all()
        self.assertEqual(len(movies), 3)

        response = self.client.get(f'{self.url}?name=the')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], 'Movie list fetched successfully.')
        self.assertEqual(len(response_body['movies']), 2)

        first_movie = response_body['movies'][0]
        self.assertEqual(first_movie['name'], "Return of the Jedi")
        self.assertFalse(first_movie['is_favorite'])
        self.assertIsNotNone(first_movie['created_at'])
        self.assertIsNotNone(first_movie['updated_at'])
        self.assertIsNotNone(first_movie['url'])
        self.assertTrue(first_movie['url'].endswith(reverse("movie_detail", args=(2,))))


class MovieDetailTest(APITestCase):

    def url(self, id: int) -> str:
        return reverse('movie_detail', args=(id,))

    def test_get_movie_detail_when_id_is_invalid__failure(self):
        response = self.client.get(self.url(id=1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_movie_detail_when_id_is_valid__success(self):
        movie_name = "Movie 1"
        release_date = "2022-05-01"
        Movie.objects.create(name=movie_name, release_date=release_date)

        response = self.client.get(self.url(id=1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], "Movie details fetched successfully.")
        self.assertEqual(response_body['details']['name'], movie_name)
        self.assertFalse(response_body['details']['is_favorite'])
        self.assertEqual(response_body['details']['release_date'], release_date)
        self.assertIsNotNone(response_body['details']['created_at'])
        self.assertIsNotNone(response_body['details']['updated_at'])


class MovieFavoriteTest(APITestCase):

    def url(self, id: int) -> str:
        return reverse('movie_favorite', args=(id, ))

    def test_add_favorite_movie_when_movie_id_is_invalid__failure(self):
        response = self.client.post(self.url(id=1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_favorite_movie_when_custom_name_is_not_in_payload__success(self):
        movie = Movie.objects.create(name="A New Hope", release_date="2022-05-01")
        self.assertFalse(movie.is_favorite)
        self.assertIsNone(movie.custom_name)

        response = self.client.post(self.url(id=1))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        movie.refresh_from_db()
        self.assertTrue(movie.is_favorite)
        self.assertIsNone(movie.custom_name)

    def test_add_favorite_movie_when_custom_name_is_in_payload__success(self):
        movie = Movie.objects.create(name="A New Hope", release_date="2022-05-01")
        self.assertFalse(movie.is_favorite)
        self.assertIsNone(movie.custom_name)

        custom_name = "new custom name"
        response = self.client.post(self.url(id=1), data={"custom_name": custom_name})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        movie.refresh_from_db()
        self.assertTrue(movie.is_favorite)
        self.assertEqual(movie.custom_name, custom_name)
