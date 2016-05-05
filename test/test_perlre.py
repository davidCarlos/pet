import unittest
import pet.perlre
import re


class TestPetPerlre(unittest.TestCase):

    def setUp(self):
        pass

    def test_if_regexp_is_empty(self):
        pattern = u''
        string = "test"

        apply_perlre_response = pet.perlre.apply_perlre(
            pattern,
            string,
        )

        self.assertEqual(string, apply_perlre_response)

    def test_if_regexp_is_not_empty(self):
        pattern = u''
        string = "test"

        apply_perlre_response = pet.perlre.apply_perlre(
            pattern,
            string,
        )

        self.assertNotEqual("testestes", apply_perlre_response)

    def test_if_pass_compile(self):
        input_re = '\\A.*/MARC-File-MARCMaker-([\\d.]+)\\.tar\\.gz\\Z'
        apply_compile = pet.perlre.compile(input_re)

        output_re = '\\A.*/MARC-File-MARCMaker-([\\d.]+)\\.tar\\.gz\\Z'
        compiled_re = re.compile(output_re)

        self.assertEqual(compiled_re, apply_compile)

    def test_if_compile_is_not_equal(self):
        input_re = '\\A.*/MARC-File-MARCMaker-([\\d.]+)\\.tar\\.gz\\Z'
        output_re = '\\A.*/MARC-FileCMaker-([\\d.]+)\\.tar\\.gz\\Z'

        compiled_re = re.compile(output_re)

        apply_compile = pet.perlre.compile(input_re)

        self.assertNotEqual(compiled_re, apply_compile)

    def test_if_pass_compile2(self):
        input_re1 = '\\A.*/File-chmod-v?(\\d[\\d.]+)'
        input_re2 = '\\.(?:tar(?:\\.gz|\\.bz2)?|tgz|zip)$\\Z'
        input_re = input_re1 + input_re2

        apply_compile = pet.perlre.compile(input_re)

        output_re1 = '\\A.*/File-chmod-v?(\\d[\\d.]+)\\.'
        output_re2 = '(?:tar(?:\\.gz|\\.bz2)?|tgz|zip)$\\Z'
        output_re = output_re1 + output_re2
        compiled_re = re.compile(output_re)

        self.assertEqual(compiled_re, apply_compile)

    def test_if_pass_not_compile2(self):
        input_re1 = '\\A.*/File-chmod-v?(\\d[\\d.]+)'
        input_re2 = '\\.(?:tar(?:\\.gz|\\.bz2)?|tgz|zip)$\\Z'
        input_re = input_re1 + input_re2

        apply_compile = pet.perlre.compile(input_re)

        output_re1 = '\\A.*/File-chmasdfasfaod-v?(\\d[\\d.]+)\\.'
        output_re2 = '(?:tar(?:\\.gz|\\.bz2)?|tgz|zip)$\\Z'
        output_re = output_re1 + output_re2
        compiled_re = re.compile(output_re)

        self.assertNotEqual(compiled_re, apply_compile)

    def test_right_apply_perlre(self):
        input_regex = "s/\+dfsg\d*$//"
        input_string = "1.9+dfsg"
        expected_result = "1.9"

        received_result = pet.perlre.apply_perlre(input_regex, input_string)

        self.assertEqual(received_result, expected_result)

    def test_if_no_match_op(self):
        input_regex = "asdfasdf//"
        input_string = "1.9+dfsg"

        with self.assertRaises(pet.exceptions.RegexpError) as cm:
            pet.perlre.apply_perlre(input_regex, input_string)
            self.assertEquals(
                "Unknown operator in regular expression '{0}'.".format(
                    input_regex
                ),
                cm.exception.message)

    def test_right_apply_perlre_regexp_dfsg(self):
        input_regex = "s/\+dfsg\d*$//"
        input_string = "1.9+dfsg"
        expected_result = "1.9"

        received_result = pet.perlre.apply_perlre(input_regex, input_string)

        self.assertEqual(received_result, expected_result)

    def test_right_apply_perlre_regexp_numbers(self):
        input_regex = "s/_(\d+)/~$1/"
        input_string = "0.008"
        expected_result = "0.008"

        received_result = pet.perlre.apply_perlre(input_regex, input_string)

        self.assertEqual(received_result, expected_result)

    def test_right_apply_perlre3(self):
        input_regex = "s/\+dfsg//"
        input_string = "1.105+dfsg"
        expected_result = "1.105"

        received_result = pet.perlre.apply_perlre(input_regex, input_string)

        self.assertEqual(received_result, expected_result)

    def test_if_last_was_escape(self):
        input_regex = "s[+dfsg\d*$/]"
        input_string = "1.106+dfsg"

        with self.assertRaises(pet.exceptions.RegexpError) as cm:
            pet.perlre.apply_perlre(input_regex, input_string)
            self.assertEquals(
                "Invalid regular expressionnn.", cm.exception.message
            )

    def test_right_apply_perlre_double_slash(self):
        input_regex = "s//+dfsg\d*$//"
        input_string = "1.106+dfsg"
        expected_result = '+dfsg\\d*$1.106+dfsg'

        received_result = pet.perlre.apply_perlre(input_regex, input_string)

        self.assertEqual(received_result, expected_result)

    def test_right_apply_perlre_with_dot_and_numbers(self):
        input_regex = "s/\.\d{5}$/$&0/"
        input_string = "2.02"
        expected_result = '2.02'

        received_result = pet.perlre.apply_perlre(input_regex, input_string)

        self.assertEqual(received_result, expected_result)

    def test_right_apply_perlre_with_dot_and_number_until_4(self):
        input_regex = "s/\.\d{4}$/$&00/"
        input_string = "2.02"
        expected_result = '2.02'

        received_result = pet.perlre.apply_perlre(input_regex, input_string)

        self.assertEqual(received_result, expected_result)

    def test_right_apply_perlre_without_doll(self):
        input_regex = "s/\~dfsg.*//"
        input_string = "0.58~dfsg"
        expected_result = '0.58'

        received_result = pet.perlre.apply_perlre(input_regex, input_string)

        self.assertEqual(received_result, expected_result)

    def test_right_apply_perlre_with_numbers_until_3(self):
        input_regex = "s/\.\d{3}$/$&000/"
        input_string = "2.02"
        expected_result = '2.02'

        received_result = pet.perlre.apply_perlre(input_regex, input_string)
        self.assertEqual(received_result, expected_result)

    def test_right_apply_perlre_with_numbers_until_4(self):
        input_regex = "s/\.\d{2}$/$&0000/"
        input_string = "2.02"
        expected_result = '2.020000'

        received_result = pet.perlre.apply_perlre(input_regex, input_string)
        self.assertEqual(received_result, expected_result)

    def test_right_apply_perlre_with_numbers_until_5(self):
        input_regex = "s/\.\d{1}$/$&00000/"
        input_string = "2.020000"
        expected_result = '2.020000'

        received_result = pet.perlre.apply_perlre(input_regex, input_string)
        self.assertEqual(received_result, expected_result)
