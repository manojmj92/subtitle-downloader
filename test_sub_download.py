'''Unit tests of subtitle_downloader'''
import unittest
import subtitle_downloader as subdl
import random
import os

class TestSubDownloader(unittest.TestCase):
    '''Unit tests for subtitle_downloader methods'''

    def test_get_subtitles(self):
        '''Positive test for method get_subtitles'''
        try:
            subs = subdl.get_subtitles("76b4703d5ace081a4f5116157751e891")
        except Exception as exep:
            self.fail("Raised {} unexpectedly!".format(exep))
        self.assertIn("Let's go home.", subs)

    def test_get_hash(self):
        '''Positive test for method get_hash'''
        tmp_file_name = "tmp_file"
        random.seed(1337)
        with open(tmp_file_name, 'w') as tmp_file:
            for _ in range(100):
                tmp_file.write(str(random.random()) * random.randint(1, 1000))
        hashed = subdl.get_hash(tmp_file_name)
        self.assertEqual("fe2cbd27befbf4c08cd611df049d0267", hashed)
        os.remove(tmp_file_name)

    def test_is_movie_extension(self):
        '''Test the is_movie_file_extention function'''
        self.assertTrue(subdl.is_movie_file_extension('.mp4'))
        self.assertFalse(subdl.is_movie_file_extension('.jpg'))

if __name__ == '__main__':
    unittest.main()
