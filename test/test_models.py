import unittest
import pet.models
import pet
from sqlalchemy.exc import OperationalError
import os.path
from mock import MagicMock

import pet.vcs


class TestPetModels(unittest.TestCase):

    def setUp(self):
        self.isfile = os.path.isfile
        self.nt1 = pet.models.NamedTree()
        self.nt1.name = "name_nt1"
        self.nt2 = pet.models.NamedTree()
        self.nt2.name = "name_nt3"
        self.ntNone = pet.models.NamedTree()
        self.ntNone.name = None
        self.namedTrees = [self.nt1, self.nt2, self.ntNone]

        self.engine = pet.engine

    def tearDown(self):
        os.path.isfile = self.isfile
        pet.engine = self.engine

    def test_check_ssl_certificate_with_file(self):
        os.path.isfile = MagicMock(return_value=True)
        pet.engine = MagicMock(return_value=True)
        engine = pet.models.check_ssl_certificate()
        self.assertIsNotNone(engine)

    def test_check_ssl_certificate_with_file_ex(self):
        os.path.isfile = MagicMock(return_value=True)
        pet.engine = MagicMock(side_effect=OperationalError("", {}, None))
        with self.assertRaises(OperationalError) as cm:
            pet.models.check_ssl_certificate()
        self.assertEquals("(NoneType) None", cm.exception.message)

    def test_check_ssl_certificate_no_file(self):
        os.path.isfile = MagicMock(return_value=False)
        pet.engine = MagicMock(return_value=True)
        engine = pet.models.check_ssl_certificate()
        self.assertIsNotNone(engine)

    def test_check_ssl_certificate_no_file_ex(self):
        os.path.isfile = MagicMock(return_value=False)
        pet.engine = MagicMock(side_effect=OperationalError("", {}, None))
        with self.assertRaises(OperationalError) as cm:
            pet.models.check_ssl_certificate()
        self.assertEquals("(NoneType) None", cm.exception.message)

    def test_get_col_spec(self):
        debversion = pet.models.DebVersion()
        self.assertEqual("DEBVERSION", debversion.get_col_spec())

    def test_bind_processor(self):
        debversion = pet.models.DebVersion()
        process = debversion.bind_processor(None)
        value = 123
        self.assertEqual(process(value), value)

    def test_result_processor(self):
        debversion = pet.models.DebVersion()
        process = debversion.result_processor(None, None)
        value = 123
        self.assertEqual(process(value), value)

    def test_vcs_if_vcs_exists(self):
        repository = pet.models.Repository()
        value = 123
        repository._vcs = value
        self.assertEqual(repository.vcs, value)

    def test_vcs_not_in_dict(self):
        repository = pet.models.Repository()
        value = 'git'
        pet.vcs.vcs_backend = MagicMock(return_value=value)
        self.assertEqual(repository.vcs, value)

    def test_package_named_trees(self):
        # Mocking chained methods
        query_rv = MagicMock()
        query_rv.filter_by = MagicMock(return_value=self.namedTrees)
        object_session_rv = MagicMock()
        object_session_rv.query = MagicMock(return_value=query_rv)
        pet.models.Session.object_session = MagicMock(
            return_value=object_session_rv
        )

        expected = {
            self.nt1.name: self.nt1,
            self.nt2.name: self.nt2,
            self.ntNone.name: self.ntNone,
        }
        actual = pet.models.Package()._named_trees('tag_or_branch')
        self.assertEqual(expected, actual)

    def test_package_branches(self):
        # Mocking chained methods
        query_rv = MagicMock()
        query_rv.filter_by = MagicMock(return_value=self.namedTrees)
        object_session_rv = MagicMock()
        object_session_rv.query = MagicMock(return_value=query_rv)
        pet.models.Session.object_session = MagicMock(
            return_value=object_session_rv
        )

        expected = {
            self.nt1.name: self.nt1,
            self.nt2.name: self.nt2,
            self.ntNone.name: self.ntNone,
        }
        actual = pet.models.Package().branches
        self.assertEqual(expected, actual)

    def test_package_tags(self):
        # Mocking chained methods
        query_rv = MagicMock()
        query_rv.filter_by = MagicMock(return_value=self.namedTrees)
        object_session_rv = MagicMock()
        object_session_rv.query = MagicMock(return_value=query_rv)
        pet.models.Session.object_session = MagicMock(
            return_value=object_session_rv
        )

        expected = {
            self.nt1.name: self.nt1,
            self.nt2.name: self.nt2,
            self.ntNone.name: self.ntNone,
        }
        actual = pet.models.Package().tags
        self.assertEqual(expected, actual)

    def test_package_trunk(self):
        # Mocking chained methods
        query_rv = MagicMock()
        query_rv.filter_by = MagicMock(return_value=self.namedTrees)
        object_session_rv = MagicMock()
        object_session_rv.query = MagicMock(return_value=query_rv)
        pet.models.Session.object_session = MagicMock(
            return_value=object_session_rv
        )

        expected = self.ntNone
        actual = pet.models.Package().trunk
        self.assertEqual(expected, actual)

    def test_models_tablenames(self):
        self.assertEqual('config', pet.models.Config.__tablename__)
        self.assertEqual('team', pet.models.Team.__tablename__)
        self.assertEqual('repository', pet.models.Repository.__tablename__)
        self.assertEqual('package', pet.models.Package.__tablename__)
        self.assertEqual('named_tree', pet.models.NamedTree.__tablename__)
        self.assertEqual('watch_result', pet.models.WatchResult.__tablename__)
        self.assertEqual('wait', pet.models.Wait.__tablename__)
        self.assertEqual('file', pet.models.File.__tablename__)
        self.assertEqual('patch', pet.models.Patch.__tablename__)
        self.assertEqual('archive', pet.models.Archive.__tablename__)
        self.assertEqual('suite', pet.models.Suite.__tablename__)
        self.assertEqual('suite_package', pet.models.SuitePackage.__tablename__)
        self.assertEqual('suite_binary', pet.models.SuiteBinary.__tablename__)
        self.assertEqual('bug_tracker', pet.models.BugTracker.__tablename__)
        self.assertEqual('bug', pet.models.Bug.__tablename__)
        self.assertEqual('bug_source', pet.models.BugSource.__tablename__)

    def test_named_tree__file(self):
        value = 2052016
        # Mocking chained methods
        query_rv = MagicMock()
        query_rv.filter_by = MagicMock(return_value=value)
        object_session_rv = MagicMock()
        object_session_rv.query = MagicMock(return_value=query_rv)
        pet.models.Session.object_session = MagicMock(
            return_value=object_session_rv
        )
        self.assertEqual(value, self.nt1._file('filename'))

    def test_named_tree_has_file_zero(self):
        mock_count = MagicMock()
        mock_count.count = MagicMock(return_value=0)
        self.nt1._file = MagicMock(return_value=mock_count)
        self.assertEqual(False, self.nt1.has_file('filename'))

    def test_named_tree_has_file_nonzero(self):
        mock_count = MagicMock()
        mock_count.count = MagicMock(return_value=100000)
        self.nt1._file = MagicMock(return_value=mock_count)
        self.assertEqual(True, self.nt1.has_file('filename'))

    def test_named_tree_file(self):
        value = 20520162
        mock_one = MagicMock()
        mock_one.one = MagicMock(return_value=value)
        self.nt1._file = MagicMock(return_value=mock_one)
        self.assertEqual(value, self.nt1.file('filename'))

    def test_named_tree_link(self):
        value = 20520163
        self.nt1.package = MagicMock()
        self.nt1.package.repository = MagicMock()
        self.nt1.package.repository.vcs = MagicMock()
        self.nt1.package.repository.vcs.link = MagicMock(return_value=value)
        self.assertEqual(value, self.nt1.link('filename'))
