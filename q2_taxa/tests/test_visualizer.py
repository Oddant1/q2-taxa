# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import tempfile
import unittest

import pandas as pd
import qiime2

from q2_taxa import barplot, tabulate


class BarplotTests(unittest.TestCase):

    def test_barplot(self):
        table = pd.DataFrame([[2.0, 2.0], [1.0, 1.0], [9.0, 8.0], [0.0, 4.0]],
                             index=['A', 'B', 'C', 'D'],
                             columns=['feat1', 'feat2'])
        taxonomy = pd.Series(['a; b; c', 'a; b; d'],
                             index=['feat1', 'feat2'])
        metadata = qiime2.Metadata(
            pd.DataFrame({'val1': ['1.0', '2.0', '3.0', '4.0']},
                         index=['A', 'B', 'C', 'D']))

        with tempfile.TemporaryDirectory() as output_dir:
            barplot(output_dir, table, taxonomy, metadata)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))
            self.assertTrue("src='lvl-1.jsonp?callback=load_data'" in
                            open(index_fp).read())


class TabulateTests(unittest.TestCase):

    def test_tabulate(self):
        taxonomy = pd.Series(['a; b; c', 'a; b; d'],
                             index=['feat1', 'feat2'])

        with tempfile.TemporaryDirectory() as output_dir:
            tabulate(output_dir, taxonomy)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))
            self.assertTrue("feat1" in open(index_fp).read())
            self.assertTrue('a; b; c' in open(index_fp).read())
