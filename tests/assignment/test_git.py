from pathlib import Path
from typing import Literal

import pytest

from assignment_submission_checker.assignment import Assignment

from .. import DATA_DIR


class TestGitDetection:
    """ """

    @pytest.fixture(scope="class")  # Does this work with subclassing??
    def placeholder_assignment(self, tool: Literal["tar", "zip"] = "tar") -> Assignment:
        """
        Standard template assignment that can be used for testing.

        It assumes the following directory and file structure is needed for the assignment:

        candidate_number/
        - assignment/
        - - .git/
        - - code_file_1.py
        - - code_file_2.py
        - - data/
        - - - data_file_1.dat
        """
        return Assignment(
            "Test assignment object",
            git_root=Path("assignment"),
            archive_tool=tool,
            expected_files=[
                "assignment/code_file_1.py",
                "assignment/code_file_2.py",
                "assignment/data/data_file_1.dat",
            ],
        )

    @pytest.fixture(
        autouse=True
    )  # Refactor this into a base class, along with the placeholder fixture above, then subclass?
    @pytest.mark.parametrize("tool", ["tar"])
    def extract_run_teardown(self, placeholder_assignment: Assignment, data_path: Path) -> None:
        """"""
        # Set the target assignment to that which was passed in
        placeholder_assignment.set_target_archive(data_path)
        # Extract the target directory to a temporary location
        placeholder_assignment.extract_to_temp_dir()
        # Run the wrapped test
        yield
        # Remove the temporary directory that was created
        placeholder_assignment.purge_tmp_dir()

    @pytest.mark.parametrize(
        "data_path, repo_should_be_found, repo_should_be_clean",
        [
            pytest.param(
                DATA_DIR / "correct_format.tar.gz",
                True,
                True,
                id="Correct repo setup",
            ),
            pytest.param(DATA_DIR / "no_git_missing_files.tar.gz", False, False, id="No git"),
            pytest.param(DATA_DIR / "dirty_git_extra_files.tar.gz", True, False, id="Dirty HEAD"),
        ],
    )
    def test_git_detection(
        self,
        placeholder_assignment: Assignment,
        repo_should_be_found: bool,
        repo_should_be_clean: bool,
    ):
        """ """

        # Run the check_for_git_root method
        obtained_result = placeholder_assignment.check_for_git_root()

        # Assert that the results were identical

        # Whether repository was found at the location provided
        assert (
            obtained_result[0] == repo_should_be_found
        ), f"Repository found at expected location: {obtained_result[0]}, but expected {repo_should_be_found}"
        # Whether the repository was clean after extraction
        assert (
            obtained_result[1] == repo_should_be_clean
        ), f"Repository was clean: {obtained_result[1]}, but expected {repo_should_be_clean}"

        # Error message when attempting to find the repository
        if repo_should_be_found:
            assert (
                obtained_result[2] == ""
            ), f"Repository should be found but obtained non-empty error string: {obtained_result[2]}"

            # Error message when determining if the repo was clean
            if repo_should_be_clean:
                assert (
                    obtained_result[3] == ""
                ), f"Repository should be clean but obtained non-empty error string: {obtained_result[3]}"
            else:
                assert (
                    obtained_result[3] != ""
                ), f"Repository should be dirty but obtained an empty error string."
        else:
            assert (
                obtained_result[2] != ""
            ), f"Repository should not be found but obtained empty error string."
