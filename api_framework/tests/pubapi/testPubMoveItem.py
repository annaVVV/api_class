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
        print "================ Cleanup ========================="
        self.utils.delete_all_except(['Documents'])

    def test_move_folder_positive(self):
        print "=======test_move_folder_positive============="
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
        print "======test_move_non_existent_folder=========="
        folder1 = self.utils.random_name()
        folder2 = self.utils.random_name()
        folder1_path = '%s/%s' % (self.config.testpath, folder1)
        self.calls.create_folder(folder1)
        resp = self.calls.move_item(name=folder2, destination=folder1_path, parent_path=self.config.testpath)
        assert resp.status_code == httplib.NOT_FOUND
        assert resp.json['errorMessage'] == "Source path for move doesn't exist"

    def test_move_folder_enough_perms_as_power_user(self):
        print "========test_move_folder_enough_perms_as_power_user============"
        # List permissions enough to move folder
        perms = ['Full', 'Owner']
        # Create 2 folders
        folder1 = self.utils.random_name()
        folder2 = self.utils.random_name()
        folder2_path = '%s/%s' % (self.config.testpath, folder2)
        folder1_path = '%s/%s' % (self.config.testpath, folder1)
        for perm1 in perms:

            for perm2 in perms:
                print '>>>>>>>>>>>>>>>Folder1 perm = %s   Folder2 perm = %s' % (perm1, perm2)
                self.calls.create_folder(folder1)
                resp = self.calls.set_perms(folder_path=folder1_path, users=self.config.puser, permission=perm1)
                assert resp.status_code == httplib.OK
                self.calls.create_folder(folder2)
                resp = self.calls.set_perms(folder_path=folder2_path, users=self.config.puser, permission=perm2)
                assert resp.status_code == httplib.OK
                resp = self.calls.move_item(name=folder1, destination=folder2_path, username=self.config.puser)
                assert resp.status_code == httplib.OK
                assert resp.json == self.no_json
                resp = self.calls.list_folders(folder_path=folder2_path)
                assert resp.json['folders'][0]['name'] == folder1
                resp = self.calls.list_folders(folder_path=folder1_path)
                assert resp.status_code == httplib.NOT_FOUND
                self.calls.delete_folder(folder2)

    def test_move_not_enough_perms_folder1(self):
        print "========test_move_not_enough_perms_folder1======="
        folder1 = self.utils.random_name()
        folder2 = self.utils.random_name()
        folder2_path = '%s/%s' % (self.config.testpath, folder2)
        folder1_path = '%s/%s' % (self.config.testpath, folder1)
        # Permissions for puser on Folder1 = >> FORBIDDEN
        perms = ['None', 'Viewer', 'Editor']
        self.calls.create_folder(folder2)
        # Permissions for puser on Folder2 = 'Full'
        resp = self.calls.set_perms(folder_path=folder2_path, users=self.config.puser, permission='Full')
        assert resp.status_code == httplib.OK
        for perm in perms:
            print '>>>>>Folder1 perm = %s   Folder2 perm = Full' % (perm)
            self.calls.create_folder(folder1)
            resp = self.calls.set_perms(folder_path=folder1_path, users=self.config.puser, permission=perm)
            assert resp.status_code == httplib.OK
            resp = self.calls.move_item(name=folder1, destination=folder2_path, username=self.config.puser)
            assert resp.status_code == httplib.FORBIDDEN
            assert resp.json['errorMessage'] == 'You do not have permission to perform this action'
            self.calls.delete_folder(folder1)
        self.calls.delete_folder(folder2)

    def test_move_not_enough_perms_folder2(self):
        print "======test_move_not_enough_perms_folder2=============="
        folder1 = self.utils.random_name()
        folder2 = self.utils.random_name()
        folder2_path = '%s/%s' % (self.config.testpath, folder2)
        folder1_path = '%s/%s' % (self.config.testpath, folder1)
        # Permissions for puser on Folder1 = 'Full'
        self.calls.create_folder(folder1)
        resp = self.calls.set_perms(folder_path=folder1_path, users=self.config.puser, permission='Full')
        assert resp.status_code == httplib.OK
        # Permissions for puser on Folder2 = >> FORBIDDEN
        perms = ['None', 'Viewer'] #, 'Editor']
        for perm in perms:
            print ' >>>>>> Folder1 perm = Full   Folder2 perm = %s' % (perm)
            self.calls.create_folder(folder2)
            resp = self.calls.set_perms(folder_path=folder2_path, users=self.config.puser, permission=perm)
            assert resp.status_code == httplib.OK
            resp = self.calls.move_item(name=folder1, destination=folder2_path, username=self.config.puser)
            assert resp.status_code == httplib.FORBIDDEN
            assert resp.json['errorMessage'] == 'You do not have permission to perform this action'
            self.calls.delete_folder(folder2)
        self.calls.delete_folder(folder1)
