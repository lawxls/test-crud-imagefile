from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from .. import models


class ModelTests(TestCase):

    def setUp(self):
        image_path = models.image_file_path(None, 'testimage.jpg')

        self.image = models.Image.objects.create(
            title='A test image',
            imagefile=image_path
        )
        self.comment = models.Comment.objects.create(
            name='YIL GUY',
            body='U have 2 YIL',
            image_post=self.image
        )

    @patch('uuid.uuid4')
    def test_image_name_uuid(self, mock_uuid):
        """Тест сохранения изображения в правильном месте"""

        uuid = 'uu-rr'
        mock_uuid.return_value = uuid

        file_path = models.image_file_path(None, 'testimage.jpg')
        exp_path = f'uploads/image/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)

    def test_image_str(self):
        """Тест str метода модели Image"""

        self.assertEqual(str(self.image), self.image.title)

    def test_comment_str(self):
        """Тест str метода модели Comment"""

        self.assertEqual(str(self.comment), self.comment.name)
