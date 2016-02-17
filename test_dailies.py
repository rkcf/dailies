import unittest
import dailies

test_task = {'name': 'test_task',
             'total': 0,
             'streak': 0,
             'max_streak': 0,
             'date_completed': 0
            }
test_task2 = {'name': 'test_task2',
              'total': 0,
              'streak': 0,
              'max_streak': 0,
              'date_completed': 0
             }
test_task3 = {'name': 'test_task3',
              'total': 0,
              'streak': 0,
              'max_streak': 0,
              'date_completed': 0
             }
test_list = [test_task, test_task2]

class DailiesHelperTest(unittest.TestCase):
    """Tests for helper functions"""
    def test_dict_in_list(self):
        self.assertTrue(dailies.dict_in_list(test_task['name'], test_list))
        self.assertFalse(dailies.dict_in_list(test_task['name'], []))
        self.assertFalse(dailies.dict_in_list(test_task3['name'], test_list))

class DailiesCommandTest(unittest.TestCase):
    """Tests for commands"""
    def test_add_task(self):
        self.assertEqual(dailies.add_task('test_task3', []), [test_task3])
        self.assertEqual(dailies.add_task('test_task', test_list), test_list)

    def test_remove_task(self):
        self.assertEqual(dailies.remove_task('test_task2', test_list), [test_task])
        self.assertEqual(dailies.remove_task('', test_list), [test_task])

    def test_complete_task(self):
        self.assertEqual(dailies.complete_task(test_task)['total'], 1)
        self.assertEqual(test_task['streak'], 1)
        self.assertEqual(test_task['max_streak'], 1)

    def tearDown(self):
        test_task = {'name': 'test_task',
                     'total': 0,
                     'streak': 0,
                     'max_streak': 0,
                     'date_completed': 0
                    }
        test_list = [test_task, test_task2]

if __name__ == '__main__':
    unittest.main
