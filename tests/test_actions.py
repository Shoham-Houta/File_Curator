import pytest
import os
from app.core import actions


class TestActions:

    def test_move(self, tmp_path):
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        source_file = source_dir / "test.txt"
        source_file.write_text("source_file")
        destination_path = tmp_path / "destination"
        destination_path.mkdir()
        destination_file = destination_path / "test.txt"

        result = actions.move_file(str(source_file), str(destination_file))
        assert result["status"] == "Success"
        assert not source_file.exists()
        assert destination_file.exists()

    def test_move_overwrite(self, tmp_path):
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        source_file = source_dir / "test.txt"
        source_file.write_text("4321")
        destination_path = tmp_path / "destination"
        destination_path.mkdir()
        destination_file = destination_path / "test.txt"
        destination_file.write_text("1234")

        result = actions.move_file(str(source_file), str(destination_file),override=True)

        assert result["status"] == "Success"
        assert not source_file.exists()
        assert destination_file.read_text() == "4321"

    def test_move_no_overwrite_fails(self, tmp_path):

        source_dir = tmp_path / "source"
        source_dir.mkdir()
        source_file = source_dir / "test.txt"
        source_file.write_text("4321")
        destination_path = tmp_path / "destination"
        destination_path.mkdir()
        destination_file = destination_path / "test.txt"
        destination_file.write_text("1234")
        result = actions.move_file(str(source_file), str(destination_file))

        assert result["status"] == "Fail"
        assert source_file.exists()
        assert destination_file.read_text() != "4321"