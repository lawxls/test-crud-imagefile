from django.test import TestCase
from unittest.mock import patch

from .. import models


class ModelTests(TestCase):

    @patch('uuid.uuid4')
    def test_image_name_uuid(self, mock_uuid):
        """Тест сохранения изображения в правильном месте"""

        uuid = 'uu-rr'
        mock_uuid.return_value = uuid

        file_path = models.image_file_path(None, 'testimage.jpg')
        exp_path = f'uploads/image/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)
