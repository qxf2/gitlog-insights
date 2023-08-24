# GitLog Insights for QA
A simple framework that provides insights derived from Git logs which can benefit testing teams. It analyzes Git repositories and generates insights that can enhance testing strategies and efficiency.

## Introduction

GitLog Insights for QA is a lightweight tool designed to provide QA teams with actionable insights extracted from Git commit history. By analyzing such data, testing teams can make informed decisions, improve testing approaches, and streamline their testing processes. The framework provides utility functions to extract and visualize data from Git logs, such as contributors, files, commits, pull requests, etc. To extract the data, it uses PyDriller, a Python framework for mining software repositories, and GitHub API.

## Insights

This project provides some utility functions that can generate insights from the data. These insights can help understand the patterns and trends in the GitHub repositories data and how they can help the testing team. Some of the insights are:

### Most modified files

### PR Review time

## Installation
To install gitlog-insights, you need to have Python 3.10 or higher and pip installed on your system. You also need to install PyDriller and its dependencies. 

1. Clone this repository:
   ```sh
   git clone https://github.com/qxf2/gitlog-insights.git
   cd gitlog-insights-for-qa

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt

## Usage
To use gitlog-qa-insights, you need to provide the path to the Git repository that you want to analyze, and optionally the start and end dates for the analysis. You can use any of the utility functions provided in the helpers folder to get the data and insights that you need. 

1. To access the GitHub API, you would need a personal access token. For information on how to create a personal access token, see "Creating a personal access token". Place the token in the config.ini file.

2. The scripts that generate insights are present in the insights folder. You can run any of the insights by using the corresponding script and providing the required arguments.
   ```
   python insights/get_most_touched_files.py qxf2/newsletter_automation 2023-01-01 2023-01-31
   ```
   You can find more details by using the --help option for each script.
   
3. Alternatively, run the main script to generate all the insights:
   ```
   python main.py

5. View the generated insights in the console.

## Examples



## License
This project is licensed under the MIT License.
