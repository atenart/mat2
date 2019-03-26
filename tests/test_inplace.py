#!/usr/bin/env python3

import unittest
import shutil
import os

from libmat2 import images, pdf

class TestInPlaceCleaning(unittest.TestCase):
    def test_jpg(self):
        shutil.copy('./tests/data/dirty.jpg', './tests/data/clean.jpg')
        p = images.JPGParser('./tests/data/clean.jpg')

        meta = p.get_meta()
        self.assertEqual(meta['Comment'], 'Created with GIMP')

        p.set_edit_in_place()
        ret = p.remove_all()
        self.assertTrue(ret)

        p = images.JPGParser('./tests/data/clean.jpg')
        self.assertEqual(p.get_meta(), {})

        os.remove('./tests/data/clean.jpg')

    def test_pdf(self):
        shutil.copy('./tests/data/dirty.pdf', './tests/data/clean.pdf')
        p = pdf.PDFParser('./tests/data/clean.pdf')

        meta = p.get_meta()
        self.assertEqual(meta['producer'], 'pdfTeX-1.40.14')

        p.set_edit_in_place()
        ret = p.remove_all()
        self.assertTrue(ret)

        p = pdf.PDFParser('./tests/data/clean.pdf')
        expected_meta = {'creation-date': -1, 'format': 'PDF-1.5', 'mod-date': -1}
        self.assertEqual(p.get_meta(), expected_meta)

        os.remove('./tests/data/clean.pdf')
