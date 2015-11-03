#!/usr/bin/env python
'''Unit tests of subtitle_downloader'''
import os
import random
import sys
import tempfile
import unittest

import subtitle_downloader as subdl

MAJOR_VERSION = sys.version_info[0]


class TestSubDownloader(unittest.TestCase):
    '''Unit tests for subtitle_downloader methods'''

    def setUp(self):
        self.tmp_path = None
        self.srt_path = None
        # Strore monkey patched function to undo safely afer each test
        self.subl_get_hash = subdl.get_hash

        def mock_log(message):
            '''Mock the logging'''
            self.logs.append(message)
        self.logs = []
        subdl.log = mock_log

    def tearDown(self):
        if self.tmp_path and os.path.isfile(self.tmp_path):
            os.remove(self.tmp_path)
        if self.srt_path and os.path.isfile(self.srt_path):
            os.remove(self.srt_path)
        subdl.get_hash = self.subl_get_hash

    def test_major_version(self):
        '''If we are not python 2 or 3, update travis ci and this test.'''
        self.assertTrue(MAJOR_VERSION in [2, 3])

    def test_get_subtitles(self):
        '''Get known subtitles from SubDb, check the content.'''
        try:
            subs = subdl.get_subtitles("76b4703d5ace081a4f5116157751e891")
        except Exception as exep:
            self.fail("Raised {0} unexpectedly!".format(exep))
        self.assertTrue("Let's go home.".encode('ascii') in subs)

    def test_get_hash(self):
        '''Positive test for method get_hash.'''
        def float_to_str(number):
            '''Converts a float to a string with 14 decimals'''
            return "%.14f" % number

        # Create a temp file with random repeatable data
        random.seed(1337)
        file_descriptor, self.tmp_path = tempfile.mkstemp()
        os.close(file_descriptor)
        with open(self.tmp_path, 'wb') as tmp_file:
            rand_data = [random.random() for _ in range(10000)]
            plaintext = " ".join(map(float_to_str, rand_data))
            if MAJOR_VERSION == 2:
                tmp_file.write(plaintext)
            elif MAJOR_VERSION == 3:
                tmp_file.write(bytes(plaintext, 'ascii'))

        hashed = subdl.get_hash(self.tmp_path)
        rand_str = float_to_str(rand_data[0])
        self.assertEqual("0.61775285695147",
                         rand_str,
                         "Random generator is not trustworthy.")
        self.assertEqual("0.61775285695147 0.53326557360500 0.36584835924938",
                         plaintext[:50],
                         "float to str conversion likely different")
        self.assertEqual("4f52910b28daeb6564c23f27d853377b", hashed,
                         "Unexpected hash calculation returned")

    def test_is_movie_extension(self):
        '''Test the is_movie_file_extention function.'''
        self.assertTrue(subdl.is_movie_file_extension('.mp4'))
        self.assertFalse(subdl.is_movie_file_extension('.jpg'))

    def test_sub_download(self):
        '''Tests the method sub_download'''
        def mock_get_hash(file_path):
            '''Return a known hash. This prevents needing a file to calculate
            the hash for this test.'''
            return "76b4703d5ace081a4f5116157751e891"

        # Monkey patch get_hash
        subdl.get_hash = mock_get_hash

        file_descriptor, self.tmp_path = tempfile.mkstemp(suffix='.mkv')
        os.close(file_descriptor)
        self.assertTrue(os.path.isfile(self.tmp_path))

        self.srt_path = subdl.sub_download(self.tmp_path)
        self.assertTrue(os.path.isfile(self.srt_path))
        with open(self.srt_path) as subs_file:
            subs = subs_file.read()
        self.assertTrue("Let's go home." in subs)
        self.assertTrue("success" in self.logs[0])

    def test_main_failure(self):
        '''Make shure main fails with not enough arguments'''
        self.assertRaises(SystemExit, subdl.main, [[]])
        self.assertTrue("at least one parameter" in self.logs[0])

if __name__ == '__main__':
    unittest.main()
