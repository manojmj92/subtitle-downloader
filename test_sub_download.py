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
    def test_major_version(self):
        '''If we are not python 2 or 3, update travis ci and this test.'''
        self.assertTrue(MAJOR_VERSION in [2, 3])

    def test_get_subtitles(self):
        '''Get known subtitles from SubDb, check the content.'''
        try:
            subs = subdl.get_subtitles("76b4703d5ace081a4f5116157751e891")
        except Exception as exep:
            self.fail("Raised {} unexpectedly!".format(exep))
        self.assertTrue("Let's go home." in subs)

    def test_get_hash(self):
        '''Positive test for method get_hash.'''
        random.seed(1337)

        file_descriptor, tmp_path = tempfile.mkstemp()
        os.close(file_descriptor)
        with open(tmp_path, 'wb') as tmp_file:
            rand_data = [random.random() for _ in range(10000)]
            plaintext = "".join(map(str, rand_data))
            if MAJOR_VERSION == 2:
                tmp_file.write(plaintext)
            elif MAJOR_VERSION == 3:
                tmp_file.write(bytes(plaintext, 'UTF-8'))
        hashed = subdl.get_hash(tmp_path)
        os.remove(tmp_path)
        rand_str = "{:16.14f}".format(rand_data[0])
        self.assertEqual("0.61775285695147", rand_str, "Random generator is not trustworthy.")
        self.assertEqual("aa35ffc8f7c7f1f8ae687e08c40c50c8", hashed)

    def test_is_movie_extension(self):
        '''Test the is_movie_file_extention function.'''
        self.assertTrue(subdl.is_movie_file_extension('.mp4'))
        self.assertFalse(subdl.is_movie_file_extension('.jpg'))

if __name__ == '__main__':
    unittest.main()
