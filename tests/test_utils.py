import unittest
import unittest.mock
from pathlib import Path

from openrelik_worker_common import utils


class Utils(unittest.TestCase):
    """Test the utils helper functions."""

    def test_dict_to_b64_string(self):
        """Test dict_to_b64_string function."""
        result = utils.dict_to_b64_string({"a": "b"})
        self.assertEqual(result, "eyJhIjogImIifQ==")

    def test_count_lines_in_file(self):
        """Test count_lines_in_file function."""
        mock_file_content = """Line1
        Line2
        Line3
        """

        file = Path('file.txt')
        file.write_text(mock_file_content, encoding="utf-8")
        lines = utils.count_lines_in_file(file.absolute())
        self.assertEqual(lines, 3)
        file.unlink()

    def test_get_input_files_input(self):
        """Test get_input_files function for input_files."""
        input_file = []
        input_file.append(utils.create_output_file("test/test"))

        result = utils.get_input_files(pipe_result=None,
                                       input_files=input_file)
        self.assertEqual(result, input_file)

    def test_get_input_files_pipe(self):
        """Test get_input_files function for pipe_result."""
        pipe_input = "eyJvdXRwdXRfZmlsZXMiOiAiL3Rlc3QvdGVzdCJ9"
        result = utils.get_input_files(pipe_result=pipe_input,
                                       input_files=None)
        expected = "/test/test"
        self.assertEqual(result, expected)

    def test_task_result(self):
        """˜Test task_result function."""
        output_files = ["a", "b"]
        workflow_id = "1234456789"
        command = "/bin/command"
        meta = {"key": "value"}

        expected = {
            "output_files": output_files,
            "workflow_id": workflow_id,
            "command": command,
            "meta": meta,
        }

        result = utils.task_result(output_files=output_files,
                                   workflow_id=workflow_id,
                                   command=command,
                                   meta=meta)
        self.assertEqual(result, utils.dict_to_b64_string(expected))

    @unittest.mock.patch("openrelik_worker_common.utils.uuid4")
    def test_create_output_file(self, mock_uuid):
        """Test create_output_file function."""

        # Generate a mocked uuid.hex()
        h = unittest.mock.MagicMock()
        h.hex = "123456789"
        mock_uuid.return_value = h

        # Test with only an output_path.
        result = utils.create_output_file(output_path="output_path/")
        self.assertEqual(result.display_name, "123456789")
        self.assertEqual(result.path, "output_path/123456789")
        self.assertEqual(result.data_type, "openrelik:worker:file:generic")

        # Test with an extra file_name.
        result = utils.create_output_file(output_path="output_path/",
                                          filename="test.txt")
        self.assertEqual(result.display_name, "test.txt")

        # Test with an extra file_extension.
        result = utils.create_output_file(output_path="output_path/",
                                          filename="test",
                                          file_extension="txt")
        self.assertEqual(result.display_name, "test.txt")

        # Test with an extra source_file_id OutputFile instance.
        source_file_id = utils.create_output_file(output_path="output_path/")
        result = utils.create_output_file(output_path="output_path/",
                                          source_file_id=source_file_id)
        self.assertEqual(result.source_file_id.uuid, source_file_id.uuid)

    @unittest.mock.patch("openrelik_worker_common.utils.uuid4")
    def test_outputfile_to_dict(self, mock_uuid):
        """Test the outputfile_to_dict function."""
        uuid = unittest.mock.MagicMock()
        uuid.hex = "123456789"
        mock_uuid.return_value = uuid

        parent_outputfile = utils.create_output_file(
            output_path="output_path/")
        outputfile = utils.create_output_file(output_path="output_path/",
                                              source_file_id=parent_outputfile)
        result = outputfile.to_dict()
        expected = {
            "filename": "123456789",
            "display_name": "123456789",
            "data_type": "openrelik:worker:file:generic",
            "uuid": "123456789",
            "path": "output_path/123456789",
            "original_path": None,
            "source_file_id": parent_outputfile,
        }
        self.assertDictEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
