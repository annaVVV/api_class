from pubapiutils import Calls
from pubapiutils import Config
from pubapiutils import Utils
import httplib
from unittest import TestCase


class TestClass(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.no_json = 'NoJSON'
        cls.calls = Calls()
        cls.config = Config()
        cls.utils = Utils()

    def setUp(self):
        self.utils.delete_all_except(['Documents'])

    def test_move_folder_positive(self):
        folder1 = self.utils.random_name()
        folder2 = self.utils.random_name()
        folder2_path = '%s/%s' % (self.config.testpath, folder2)
        folder1_path = '%s/%s' % (self.config.testpath, folder1)
        self.calls.create_folder(folder1)
        self.calls.create_folder(folder2)
        resp = self.calls.move_item(name=folder1, destination=folder2_path)
        assert resp.status_code == httplib.OK
        assert resp.json == self.no_json
        resp = self.calls.list_folders(folder_path=folder2_path)
        assert resp.json['folders'][0]['name'] == folder1
        resp = self.calls.list_folders(folder_path=folder1_path)
        assert resp.status_code == httplib.NOT_FOUND

    def test_move_non_existent_folder(self):
        folder1 = self.utils.random_name()
        folder2 = self.utils.random_name()
        folder1_path = '%s/%s' % (self.config.testpath, folder1)
        self.calls.create_folder(folder1)
        resp = self.calls.move_item(name=folder2, destination=folder1_path, parent_path=self.config.testpath)
        assert resp.status_code == httplib.NOT_FOUND
        assert resp.json['errorMessage'] == "Source path for move doesn't exist"