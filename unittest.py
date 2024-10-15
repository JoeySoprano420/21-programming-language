import unittest
from MLPlus import MLPlusAlgorithm, HybridDatabase

class TestMLPlus(unittest.TestCase):

    def setUp(self):
        self.db = HybridDatabase()
        self.ml_algorithm = MLPlusAlgorithm()

    def test_insert_data(self):
        result = self.db.insert_data("test_key", "test_value")
        self.assertEqual(result, "Data successfully processed and stored.")
        self.assertEqual(self.db.query_data("test_key"), "test_value")

    def test_query_non_existent_data(self):
        result = self.db.query_data("non_existent_key")
        self.assertEqual(result, "No data found.")

    def test_learning_and_classifying(self):
        self.ml_algorithm.learn("example", "classification")
        self.assertEqual(self.ml_algorithm.classify("example"), "classification")
        self.assertEqual(self.ml_algorithm.classify("unknown"), "Unknown")

if __name__ == '__main__':
    unittest.main()
