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
        self.assertTrue("Let's go home.".encode('ascii') in subs)

    def test_get_hash(self):
        '''Positive test for method get_hash.'''
        def float_to_str(number):
            '''Converts a float to a string with 14 decimals'''
            return "%.14f" % number

        # Create a temp file with random repeatable data
        random.seed(1337)
        file_descriptor, tmp_path = tempfile.mkstemp()
        os.close(file_descriptor)
        with open(tmp_path, 'wb') as tmp_file:
            rand_data = [random.random() for _ in range(10000)]
            plaintext = " ".join(map(float_to_str, rand_data))
            tmp_file.write(bytes(plaintext, 'ascii'))

        hashed = subdl.get_hash(tmp_path)
        os.remove(tmp_path)
        rand_str = float_to_str(rand_data[0])
        self.assertEqual("0.61775285695147", rand_str, "Random generator is not trustworthy.")
        self.assertEqual("0.61775285695147 0.53326557360500 0.36584835924938", plaintext[:50],
                         "float to str conversion likely different")
        self.assertEqual("4f52910b28daeb6564c23f27d853377b", hashed,
                         "Unexpected hash calculation returned")

    def test_is_movie_extension(self):
        '''Test the is_movie_file_extention function.'''
        self.assertTrue(subdl.is_movie_file_extension('.mp4'))
        self.assertFalse(subdl.is_movie_file_extension('.jpg'))

if __name__ == '__main__':
    unittest.main()
