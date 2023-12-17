import unittest
import logging
import pycommon as M


class TestMylog(unittest.TestCase):
    def test_log(self):
        with self.assertLogs() as cm:
            M.log()
            logging.info('coucou')
        self.assertListEqual(cm.output, ['INFO:root:coucou'])

    def test_debug(self):
        with self.assertLogs() as cm:
            M.log()
            M.debug('coucou')
        self.assertListEqual(cm.output, ['INFO:aoc:coucou'])

    def test_nolog(self):
        with self.assertLogs() as cm:
            M.log()
            M.debug('coucou')
            M.nolog()
            M.debug('ouioui')
            M.log()
            M.debug('nonnon')
        self.assertListEqual(cm.output, ['INFO:aoc:coucou', 'INFO:aoc:nonnon'])

    def test_is_log_enable(self):
        self.assertTrue(M.is_log_enable())
        M.log()
        self.assertTrue(M.is_log_enable())
        M.nolog()
        self.assertFalse(M.is_log_enable())
        M.log()
        self.assertTrue(M.is_log_enable())





if __name__ == '__main__':
    unittest.main()
