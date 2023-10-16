"""
This script fetches the most modified files in a GitHub repository based on
start_date, end_date, repo, branch, file_type

"""
import sys
import git
from typing import Optional
import heapq
from collections import defaultdict
import pandas as pd
from pydriller import Repository

def find_top_files(
    repo_path: str,
    start_date: str,
    end_date: str,
    file_type: Optional[str],
    branch: str,
    num_files: int = 5,
):
    """
    Find the top files in a repository based on the number of modifications.

    Args:
        repo_path (str): The path to the repository.
        start_date (str): The start date for filtering commits.
        end_date (str): The end date for filtering commits.
        branch (str): The branch to consider for commits.
        file_type (str, optional): The file type to filter. Defaults to None.

    Returns:
        dataframe: A dataframe containing the file info.
    """

    file_count = defaultdict(int)
    file_info = defaultdict(
        lambda: {"authors": set(), "messages": [], "dates": [], "complexity": None}
    )
    try:
        commit_list = Repository(
            repo_path, since=start_date, to=end_date, only_in_branch=branch
        ).traverse_commits()

        for commit in commit_list:
            for file in commit.modified_files:
                file_name = file.filename
                if not file_type or file_name.endswith(file_type):
                    file_info[file_name]["authors"].add(commit.author.name)
                    if commit.committer_date is not None:
                        date_str = commit.committer_date.strftime("%Y-%m-%d %H:%M:%S")
                        file_info[file_name]["dates"].append(date_str)
                    file_info[file_name]["messages"].append(commit.msg)
                    file_info[file_name]["complexity"] = (
                        file.complexity if not pd.isna(file.complexity) else "NA"
                    )
                    file_count[file_name] += 1

        pd.set_option("display.max_column", None)

        top_files = heapq.nlargest(num_files, file_count.items(), key=lambda x: x[1])
        data = []

        for file, count in top_files:
            file_dict = {
                "File": file,
                "Count": count,
                "Complexity": file_info[file]["complexity"],
                "Authors": ", ".join(file_info[file]["authors"]),
                "Last Commit Message": file_info[file]["messages"][-1],
                "Last Commit Date": file_info[file]["dates"][-1],
            }
            data.append(file_dict)

        file_info_df = pd.DataFrame(data)
        return file_info_df
    except git.exc.NoSuchPathError as error:
        print(f"\nCaught NoSuchPathError: {error}\n")
        sys.exit(1)
    except git.exc.GitCommandError as error:
        if error.status == 128:
            print("\nError : Default branch is not main for this repo!(Try master)\n")
            print(f"Error message: {error}")
            sys.exit(1)
        else:
            print(f"\nCaught a different GitCommandError : {error}\n")
            sys.exit(1)
    except OSError as error:
        print(f"\nCaught an OSError: {error}\n")
        sys.exit(1)
    except Exception as general_error:
        print(f"\nError occurred: {general_error}\n")
        sys.exit(1)