import unittest
import os
import shutil
from unittest.mock import patch
from datetime import datetime
from app.create_file import create_directory, create_file

class TestCreateFile(unittest.TestCase):

    def setUp(self):
        """Create a test directory before each test."""
        self.test_dir = "test_dir"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def tearDown(self):
        """Remove the test directory after each test."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_create_directory(self):
        """Test directory creation."""
        path_list = [self.test_dir, "subdir1", "subdir2"]
        result = create_directory(path_list)
        expected_path = os.path.join(*path_list)
        self.assertEqual(result, expected_path)
        self.assertTrue(os.path.exists(expected_path))

    @patch("builtins.input", side_effect=["Enter content line 1", "Enter content line 2", "Enter content line 3", "stop"])
    @patch('app.create_file.datetime')
    def test_create_file(self, mock_datetime, mock_input):
        mock_datetime.now.return_value = datetime(2022, 2, 1, 14, 41, 10)  # Mock datetime
        file_name = os.path.join(self.test_dir, "test_file.txt")

        create_file(file_name)

        self.assertTrue(os.path.exists(file_name))

        with open(file_name, "r") as f:
            lines = f.readlines()
            print("DEBUG: Lines from file:", lines)  # Debug output

            self.assertIn("2022-02-01 14:41:10", lines[0])
            self.assertEqual(lines[1], "1 Enter content line 1\n")
            self.assertEqual(lines[2], "2 Enter content line 2\n")
            self.assertEqual(lines[3], "3 Enter content line 3\n")

    @patch("builtins.input",
           side_effect=["Enter content line 1", "Enter content line 2", "Enter content line 3", "stop"])
    @patch('app.create_file.datetime')
    def test_append_to_existing_file(self, mock_datetime, mock_input):
        """Test appending content to an existing file."""
        mock_datetime.now.return_value = datetime(2022, 2, 1, 14, 41, 10)  # Mock datetime
        file_name = os.path.join(self.test_dir, "test_file.txt")

        create_file(file_name)

        mock_datetime.now.return_value = datetime(2022, 2, 1, 14, 46, 1)
        mock_input.side_effect = ["Another line 1", "Another line 2", "Another line 3", "stop"]
        create_file(file_name)

        with open(file_name, "r") as f:
            lines = f.readlines()
            print("DEBUG: Lines from file after append:", lines)  # Debug output

            self.assertIn("2022-02-01 14:41:10", lines[0])
            self.assertEqual(lines[1], "1 Enter content line 1\n")
            self.assertEqual(lines[2], "2 Enter content line 2\n")
            self.assertEqual(lines[3], "3 Enter content line 3\n")

            self.assertIn("2022-02-01 14:46:01", lines[4])
            self.assertEqual(lines[5], "1 Another line 1\n")
            self.assertEqual(lines[6], "2 Another line 2\n")
            self.assertEqual(lines[7], "3 Another line 3\n")
