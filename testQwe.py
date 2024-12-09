import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
from qwe import create_gui, handle_command, ls, cd, chown, whoami, virtual_fs, current_path, current_user, computer_name

class TestVirtualOSCommands(unittest.TestCase):

    def setUp(self):
        global current_path
        current_path = ["God", "home"]

    def test_ls_command(self):
        output = ls(current_path)
        self.assertIn("user", output)
        self.assertIn("admin", output)

    def test_cd_command(self):
        global current_path
        current_path = ["God", "home"]
        cd(current_path, "user")
        self.assertEqual(current_path, ["God", "home", "user"])

        current_path = ["God", "home", "user"]
        cd(current_path, "..")
        self.assertEqual(current_path, ["God", "home"])

    def test_chown_command(self):
        global current_path
        current_path = ["God", "home", "user"]
        chown(current_path, "file1.txt", "new_owner")
        self.assertEqual(virtual_fs["God"]["home"]["user"]["file1.txt"], "new_owner")

    def test_whoami_command(self):
        output = whoami()
        self.assertEqual(output, current_user)

    def test_unknown_command(self):
        output_text = MagicMock()
        handle_command("unknown_command", output_text)
        output_text.insert.assert_called_with(tk.END, "Unknown command\n")

if __name__ == "__main__":
    unittest.main()
