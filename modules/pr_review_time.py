""""
This script fetches the PR review time of all closed PR's for a given time period
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.github_pr_data_extractor import PRDataExtractor
import pandas as pd

def calculate_review_time(repo_name, start_date, end_date):
    """
    Gets the PR review details and calculates the total review time for each PR.
    It also computes the average review time for the given time period
    """

    try:
        github_api = PRDataExtractor(repo_name)
        pr_details = github_api.get_merged_pr_details(start_date, end_date)

        if pr_details.empty:
            return pd.DataFrame()

        pr_details['created_at'] = pd.to_datetime(pr_details['created_at'],errors='coerce')
        pr_details['closed_at'] = pd.to_datetime(pr_details['closed_at'],errors='coerce')
        pr_details = pr_details[pr_details['status'] == 'closed']

        pr_details['review_time'] = pr_details['closed_at'] - pr_details['created_at']

        return pr_details
    except Exception as error:
        print(f"An error occurred: {error}")
        return pd.DataFrame()
    

def compute_inference(review_details):
    """
    Calculates the average review time for a set of pull requests (PRs) and 
    computes inference.

    Args:
        review_details (DataFrame): A DataFrame containing information about pull requests

    Returns:
        average_review_time (float): The average review time for the pull requests.
        long_review_prs (DataFrame): A DataFrame containing information about the 
        pull requests with review times longer than the average.
    """
    try:
        average_review_time = review_details['review_time'].mean()
    except Exception as e:
        print(f"Error calculating average review time: {e}")
        average_review_time = 0

    print("\nInsights for the timeperiod :")

    long_review_prs = review_details[review_details['review_time'] > average_review_time]

    print(f"\n -> The average time taken to review PR: {average_review_time}")

    if not long_review_prs.empty:
        print("\n -> The following PRs took longer than average time:")
        for index, row in long_review_prs.iterrows():
            print(f" ** PR #{row['pr_number']}: {row['pr_title']} - Review Time: {row['review_time']}")
            
    # Find the author with the most reviews
    most_reviews_author = review_details['author'].value_counts().idxmax()
    print(f"\n -> Author with the most PR's': {most_reviews_author}")

    # Find the author with the most average review time
    avg_time_by_author = review_details.groupby('author')['review_time'].mean()
    most_avg_time_author = avg_time_by_author.idxmax()
    print(f"\n -> Author with the highest average review time: {most_avg_time_author}")
    return average_review_time, long_review_prs