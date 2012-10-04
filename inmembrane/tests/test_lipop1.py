import os
import unittest
import sys

import inmembrane
import inmembrane.tests
from inmembrane import helpers
from inmembrane.plugins import lipop1

class TestLipoP(unittest.TestCase):
  def setUp(self):
      self.dir = os.path.join(
         os.path.abspath(
         os.path.dirname(inmembrane.tests.__file__)), 'lipop1')

  def test_lipop(self):
    save_dir = os.getcwd()
    os.chdir(self.dir)

    helpers.silence_log(True)
    helpers.clean_directory('.', ['input.fasta'])
   
    self.params = inmembrane.get_params()
    if not self.params['lipop1_bin']:
      self.params['lipop1_bin'] = 'LipoP'
    self.params['fasta'] = "input.fasta"
    self.seqids, self.proteins = \
        helpers.create_proteins_dict(self.params['fasta'])

    lipop1.annotate(self.params, self.proteins)

    self.expected_output = {
        u'SPy_0252': True,
        u'SPy_2077': False, 
        u'SPy_0317': True,
        u'tr|Q9HYX8' : True,
    }
    
    for seqid in self.expected_output:
      self.assertEqual(
          self.expected_output[seqid], self.proteins[seqid]['is_lipop'])
    self.assertEqual(self.proteins[u'tr|Q9HYX8']['lipop_cleave_position'], 19)
    self.assertIn('lipop_im_retention_signal', self.proteins[u'tr|Q9HYX8'])
    self.assertTrue(self.proteins[u'tr|Q9HYX8']['lipop_im_retention_signal'])
    os.chdir(save_dir)


if __name__ == '__main__':
  unittest.main()
