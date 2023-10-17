from pathlib import Path

import pytest

from assignment_submission_checker.assignment import Assignment

from .. import DATA_DIR, placeholder_assignment


@pytest.mark.parametrize(
    "data, repo_should_be_found, repo_should_be_clean",
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
def test_git_root(
    placeholder_assignment: Assignment,
    data: Path,
    repo_should_be_found: bool,
    repo_should_be_clean: bool,
) -> None:
    """
    Test that the check_for_git_root method correctly:
    - Identifies a git repository in the specified location
    - Identifies the absence of such a repository
    - Identifies if the repository is dirty
    """
    # Set target data file so that extracted file has expected structure
    placeholder_assignment.set_target_archive(data)
    # Extract
    placeholder_assignment.extract_to_temp_dir()

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

    # Clean up extracted files
    placeholder_assignment.purge_tmp_dir()
