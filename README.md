# GitLog Insights for QA
A simple framework that provides insights derived from Git logs which can benefit testing teams. 

## Introduction

GitLog Insights is designed to provide QA teams with actionable insights extracted from Git commit history. By analyzing such data, testing teams can make informed decisions, improve testing approaches, and streamline their testing processes. The framework provides utility functions to extract and visualize data from Git logs, such as contributors, files, commits, pull requests, etc. To extract the data, it uses [PyDriller](https://github.com/ishepard/pydriller), a Python framework for mining software repositories, and [GitHub API](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api?apiVersion=2022-11-28).

## Installation
To install and run this project, you need to have Python 3.8 or higher and pip installed on your system. You also need to install PyDriller and its dependencies.

<ul>
   
1. Clone this repository:
   ```sh
   git clone https://github.com/qxf2/gitlog-insights.git
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   
3. Set Up API Keys
   Some of the insights (the ones which accesses GitHub API to fetch data) need a personal access token.
   For information on how to create a personal access token, see [Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token).

   ```sh
   export API_KEY=<your-key>
   ```
</ul>

## Running Insights
The scripts that generate insights are present in the insights folder. You can run any of the insights by using the corresponding script and providing the required arguments. The arguments are the time period within which you want to run the insight - start_date and end_date. And the Git Repository you want to analyze.

Some of the insights are:

#### Top Touched files

Find the top files that have been modified the most in a given time period.

```
gitlog-insights$ python insights/top_touched_files.py

Enter the start date (YYYY-MM-DD): 2023-07-05
Enter the end date (YYYY-MM-DD): 2023-07-30
Enter the repository path (https://github.com/<repo_name>.git): https://github.com/qxf2/qxf2-page-object-model.git
Enter the branch name (default: main): master
Enter the file type extension (starting with .) (default: all):
Defaulting to all files.

Insights for the duration 2023-07-05 to 2023-07-30:

  -> One of the top modified files having a high complexity of 178 is: Base_Page.py
  -> The file(s) that had maximum commits (precisely 1) are: ['Base_Page.py', 'driverfactory.py', 'remote_options.py']
  -> Author(s) who made these 1 commits are: ['Avinash Shetty']
```

#### PR Review time

```
gitlog-insights$ python insights/pr_review_time.py

Enter the start date (YYYY-MM-DD): 2023-09-10
Enter the end date (YYYY-MM-DD): 2023-09-30
Enter the repository name: pallets/flask

Insights for the timeperiod :

 -> The average time taken to review PR:  7 days 09:45:10.333333333

 -> The following PRs took longer than average time:
 ** PR #5257: Release version 3.0.0 - Review Time: 13 days 23:35:42

 -> Author with the most PR's': pgjones

 -> Author with the highest average review time:  pgjones

Detailed report can be found in pr_review_time_report.html
```

#### Author Bias
```
gitlog-insights$ python insights/author_bias_insights.py

Enter the start date (YYYY-MM-DD): 2023-12-10
Enter the end date (YYYY-MM-DD): 2023-12-20
Enter the repository path (For example: https://github.com/qxf2/qxf2-page-object-model.git ):https://github.com/Pythagora-io/gpt-pilot

 Files with High Author Bias during the time period:

 -> create_readme.prompt
 -> ipc.py
 -> feature.py
 -> test_cli.py
 -> function_calls.py

Detailed report can be found in report_author_bias.html (in reports folder)
```

#### Size of PRs

```
gitlog-insights$ python insights/size_of_prs.py

Enter the start date (YYYY-MM-DD): 2023-02-02
Enter the end date (YYYY-MM-DD): 2023-02-20
Enter the repository name: qxf2/newsletter_automation

Insights for the time period:

 -> The PR#208 has maximum number of code lines changed: 427 lines.

 -> The PR#204 has maximum number of files changed: 25 changes.

Detailed report can be found in size_of_prs_report.html
```
#### Merge Activity

```

```




## Examples



## License
This project is licensed under the MIT License.
