"""
This script helps in extracting pull request data from GitHub.
"""

import os
import logging
import sys
import pandas as pd
import requests
from .github_data_extractor import GitHubDataExtractor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



class PRDataExtractor(GitHubDataExtractor):
    """
    The `PRDataExtractor` class is a subclass of the `GitHubDataExtractor` class and
    is used to extract data related to pull requests from GitHub using the GitHub API.
    """
    @property
    def endpoint(self):
        """
        Returns:
            str: The endpoint URL for the GitHub API to search for issues.
        """
        endpoint = f"{self.base_url}/search/issues"
        return endpoint

    def create_query(self, start_date, end_date):
        """
        Returns a query string for searching pull requests on GitHub based on the repo name
        and a specified date range.
        Args:
            start_date (str): The start date of the date range for the pull requests.
            end_date (str): The end date of the date range for the pull requests.
        Returns:
            str: The query string for searching pull requests on GitHub.
        """
        query = f"is:pr repo:{self.repo_name} created:{start_date}..{end_date}"
        return query

    def get_pr_details(self, start_date, end_date):
        """
        Retrieve details of pull requests from GitHub within a specified date range.
        Args:
            start_date (str): The start date of the date range for the pull requests.
            end_date (str): The end date of the date range for the pull requests.
        Returns:
            pandas DataFrame: Containing the details of the pull requests.
        """
        query = f"is:pr repo:{self.repo_name} created:{start_date}..{end_date}"
        return self.get_pr_details_using_query(query)

    def get_merged_pr_details(self, start_date, end_date):
        """
        Retrieves details of merged pull requests from GitHub within a specified date range.
        Args:
            start_date (str): The start date of the date range for the merged pull requests.
            end_date (str): The end date of the date range for the merged pull requests.
        Returns:
            DataFrame: Containing the details of the merged pull requests.
        """
        query = f"is:pr is:merged repo:{self.repo_name} merged:{start_date}..{end_date}"
        return self.get_pr_details_using_query(query)

    def get_pr_details_using_query(self, query):
        """
        Retrieves details of pull requests from GitHub based on a specified query.
        Args:
            query (str): The query string for searching pull requests on GitHub.
        Returns:
            DataFrame: Containing the details of the pull requests matching the query.
        """
        try:
            params = {"q": query}
            response = requests.get(self.endpoint, headers=self.header, params=params)
            self.validate_response(response)

            pr_data = response.json().get("items", [])

            if not pr_data:
                print("No data found within the specified date range.")
                return pd.DataFrame()

            pr_list = []
            for pull_request in pr_data:
                pr_dict = {
                    "pr_number": pull_request["number"],
                    "pr_title": pull_request["title"],
                    "created_at": pull_request["created_at"],
                    "author": pull_request["user"]["login"],
                    "status": pull_request["state"],
                    "closed_at": (
                        pull_request["closed_at"]
                        if pull_request["state"] == "closed"
                        else "N/A"
                    ),
                }
                pr_list.append(pr_dict)

            pr_df = pd.DataFrame(pr_list)
            return pr_df
        except requests.exceptions.RequestException as error:
            logging.error("An error occurred: %s", error)
            raise error

    def get_pr_files_details(self, start_date, end_date):
        """
        Retrieves details of the files associated with pull requests from GitHub
        within a specified date range.
        Args:
            start_date (str): The start date of the date range for the pull requests.
            end_date (str): The end date of the date range for the pull requests.
        Returns:
            DataFrame: A pandnas DataFrame containing the details of the files.
        """
        try:
            params = {"q": self.create_query(start_date, end_date)}
            response = requests.get(self.endpoint, headers=self.header, params=params)
            self.validate_response(response)

            pr_data = response.json().get("items", [])

            pr_files_list = []
            for pull_request in pr_data:
                pr_number = pull_request["number"]

                files_details = self.extract_files_data(pr_number)

                for file_dict in files_details:
                    file_dict["pr_number"] = pr_number
                    pr_files_list.append(file_dict)

            pr_files_df = pd.DataFrame(pr_files_list)
            return pr_files_df
        except requests.exceptions.RequestException as error:
            logging.error("An error occurred: %s", error)
            raise error

    def extract_files_data(self, pr_number):
        """
        Retrieve details of the files associated with a pull request from GitHub.
        Args:
            pr_number (int): The number of the pull request for which to retrieve file details.
        Returns:
            list: A list of dictionaries, where each dictionary represents the details of a file
            associated with the pull request.
        """
        try:
            endpoint = f"{self.base_url}/repos/{self.repo_name}/pulls/{pr_number}/files"
            response = requests.get(endpoint, headers=self.header)
            self.validate_response(response)

            files_data = response.json()

            files_details = []

            for file in files_data:
                file_dict = {
                    "filename": file["filename"],
                    "status": file["status"],
                    "additions": file["additions"],
                    "deletions": file["deletions"],
                    "changes": file["changes"],
                }

                files_details.append(file_dict)

            return files_details
        except requests.exceptions.RequestException as error:
            logging.error("An error occurred: %s", error)
            raise error
