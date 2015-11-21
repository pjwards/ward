from django.test import TestCase

from archive.fb.fb_lookup import lookup_id


class FbLookupTests(TestCase):
    def test_lookup_id_with_url(self):
        """
        lookup_id should return correct id for correct url or None for wrong url.

        :return: id or None
        """
        codingeverybody_url = "https://www.facebook.com/groups/codingeverybody/"
        codingeverybody_id = "174499879257223"
        self.assertEqual(lookup_id(codingeverybody_url), codingeverybody_id)

        wrong_url = "https://www.google.com"
        self.assertEqual(lookup_id(wrong_url), None)
