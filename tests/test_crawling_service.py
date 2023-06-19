import unittest
from app.service import ScrawlingService
from unittest.mock import MagicMock

class TestCrawlingService(unittest.TestCase):
    def test_get_some_app_urls_in_page(self):
        mock_anchor = MagicMock()
        mock_anchor.get_attribute.return_value = 'https://apps.apple.com/my/app/todai-learn-spanish-by-news/id6446880636'
        mocked_set_of_targeted_urls = set()
        mock_anchors = [mock_anchor, mock_anchor, mock_anchor]

        ScrawlingService.get_app_urls_in_page(mocked_set_of_targeted_urls, mock_anchors)

        expected_result = {'https://apps.apple.com/my/app/todai-learn-spanish-by-news/id6446880636'}
        self.assertEqual(mocked_set_of_targeted_urls, expected_result)

    def test_get_none_app_url_in_page(self):
        mock_anchor = MagicMock()
        mock_anchor.get_attribute.return_value = None
        mocked_set_of_targeted_urls = set()
        mock_anchors = [mock_anchor]

        ScrawlingService.get_app_urls_in_page(mocked_set_of_targeted_urls, mock_anchors)

        empty_set = set()
        self.assertEqual(mocked_set_of_targeted_urls, empty_set)

    def test_get_a_destination_page(self):
        mock_random_anchor = MagicMock()
        mock_random_anchor.get_attribute.return_value = 'https://apps.random.com/super-random'
        mock_apple_anchor = MagicMock()
        mock_apple_anchor.get_attribute.return_value = 'https://apps.apple.com/my/developer/ghi-nguyen/id933081416'
        all_mock_anchors = [mock_random_anchor, mock_apple_anchor]

        result_apple_link = ScrawlingService.get_destination_page(all_mock_anchors)

        self.assertEqual(result_apple_link, 'https://apps.apple.com/my/developer/ghi-nguyen/id933081416')

    def test_get_no_destination_page(self):
        mock_random_anchor = MagicMock()
        mock_random_anchor.get_attribute.return_value = 'https://apps.random.com/super-random'
        all_mock_anchors = [mock_random_anchor, mock_random_anchor]

        result_apple_link = ScrawlingService.get_destination_page(all_mock_anchors)
        
        self.assertEqual(result_apple_link, None)
