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
   
3. Set Up TOKEN
   Some of the insights (the ones which accesses GitHub API to fetch data) need a personal access token.
   For information on how to create a personal access token, see [Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token).

   ```sh
   export TOKEN=<your-token>
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
Enter the repository path: https://github.com/qxf2/qxf2-page-object-model.git
Enter the branch name (default: main): master
Enter the file type extention (starting with .) (default: all):
Defaulting to all files.

Insights for the duration 2023-07-05 to 2023-07-30:

  -> One of the top modified files having a high complexity of 178 is: Base_Page.py
  -> The file(s) that had maximum commits (precisely 1) are: ['Base_Page.py', 'driverfactory.py', 'remote_options.py']
  -> Author(s) who made these 1 commits are: ['Avinash Shetty']

Detailed report can be found in top_touched_files_report.html
```

#### PR Review time

```
gitlog-insights$ python insights/pr_review_time.py

Enter the start date (YYYY-MM-DD): 2019-02-02
Enter the end date (YYYY-MM-DD): 2020-02-02
Enter the repository name: qxf2/qxf2-page-object-model

Insights for the timeperiod :

 -> The average time taken to review PR:  11 days 05:53:28.800000

 -> The following PRs took longer than average time:
 ** PR #175: Convert screenshots to gif - Review Time: 12 days 20:45:29
 ** PR #152: Int to string util - Review Time: 13 days 22:47:31
 ** PR #142: Stop test exception - Review Time: 13 days 23:26:09
 ** PR #133: Report portal integration - Review Time: 210 days 04:07:00
 ** PR #111: Loguru implementation in our POM - Review Time: 16 days 16:24:16

 -> Author with the most PR's': nilaya123

 -> Author with the highest average review time:  nilaya123

Detailed report can be found in pr_review_time_report.html
```

#### Author Bias
```
gitlog-insights$ python insights/author_bias_insights.py

Enter the start date (YYYY-MM-DD): 2018-02-02
Enter the end date (YYYY-MM-DD): 2020-02-02
Enter the repository path: https://github.com/qxf2/qxf2-page-object-model.git

 Files with High Author Bias during the time period:

 -> Bitcoin Info_com.dudam.rohan.bitcoininfo.apk
 -> remote_credentials_enc.py
 -> .gitignore
 -> testrail_caseid_conf.py
 -> example_table_conf.py

Detailed report can be found in report_author_bias.html
```

#### Size of PRs

```
gitlog-insights$ python insights/size_of_prs.py

Enter the start date (YYYY-MM-DD): 2019-05-01
Enter the end date (YYYY-MM-DD): 2020-05-01
Enter the repository name: qxf2/qxf2-page-object-model

Insights for the time period:

 -> The PR#186 has maximum number of code lines changed: 1235 lines.

 -> The PR#186 has maximum number of files changed: 30 changes.

Detailed report can be found in size_of_prs_report.html
```
#### Merge Activity

```
gitlog-insights$ python insights/merge_activity.py

Enter the start date (YYYY-MM-DD): 2018-02-02
Enter the end date (YYYY-MM-DD): 2019-03-03
Enter the repository name: qxf2/qxf2-page-object-model

Insights for the timeperiod :

The maximum number of merges during the specified period was: 4

These occured on the following days of the week:
   -> Wednesday, 2018-February: 4
   -> Friday, 2018-May: 4
   -> Friday, 2019-February: 4

Detailed report can be found in merge_activity_report.html

```



## License
This project is licensed under the MIT License.
