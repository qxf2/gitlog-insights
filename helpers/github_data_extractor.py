"""
This script defines a class that extracts data from GitHub using the GitHub API.
The class takes a repository name as an argument and initializes an instance with that name.
"""

import os
import logging
from requests.exceptions import HTTPError

logging.basicConfig(filename='error.log', level=logging.ERROR)

class GitHubDataExtractor:
    """
    Extracts data from GitHub using the GitHub API.
    """
    base_url = "https://api.github.com"

    def __init__(self, repo_name):
        """
        Initializes the GitHubDataExtractor class with a repository name.
        """
        self.repo_name = repo_name

    @property
    def token(self):
        """
        Retrieves the access token from the environment variable.
        """
        token = os.environ.get('TOKEN')
        return token

    @property
    def header(self):
        """
        Sets the request header with the access token and the desired API version.
        """
        header = {
            'Authorization': f"Bearer {self.token}",
            'Accept': 'application/vnd.github.v3+json',
        }
        return header

    def validate_response(self, response):
        """
        Validates the response from the API by checking the status code.
        """
        if response.status_code == 200:
            return True
        raise HTTPError(f"Error: {response.status_code}")
        