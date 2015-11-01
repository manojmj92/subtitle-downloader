#!/usr/bin/env python
'''Unit tests of subtitle_downloader'''
import os
import random
import sys
import tempfile
import unittest

import subtitle_downloader as subdl

class TestSubDownloader(unittest.TestCase):
    '''Unit tests for subtitle_downloader methods'''
    def test_print_version(self):
        '''If we are not python 2 or 3, update travis ci and this test'''
        print(sys.version_info)
        major_version = sys.version_info.major
        self.assertIn(major_version, [2, 3])

    def test_get_subtitles(self):
        '''Positive test for method get_subtitles'''
        try:
            subs = subdl.get_subtitles("76b4703d5ace081a4f5116157751e891")
        except Exception as exep:
            self.fail("Raised {} unexpectedly!".format(exep))
        self.assertIn("Let's go home.", subs)

    def test_get_hash(self):
        '''Positive test for method get_hash'''
        random.seed(1337)

        file_descriptor, tmp_path = tempfile.mkstemp()
        os.close(file_descriptor)
        with open(tmp_path, 'w+b') as tmp_file:
            for _ in range(100):
                tmp_file.write(str(random.random()) * random.randint(1, 1000))
        hashed = subdl.get_hash(tmp_path)
        os.remove(tmp_path)
        self.assertEqual("fe2cbd27befbf4c08cd611df049d0267", hashed)

    def test_is_movie_extension(self):
        '''Test the is_movie_file_extention function'''
        self.assertTrue(subdl.is_movie_file_extension('.mp4'))
        self.assertFalse(subdl.is_movie_file_extension('.jpg'))

if __name__ == '__main__':
    unittest.main()
