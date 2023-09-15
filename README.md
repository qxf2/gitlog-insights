# GitLog Insights for QA
A simple framework that provides insights derived from Git logs which can benefit testing teams. It analyzes Git repositories and generates insights that can enhance testing strategies and efficiency.

## Introduction

GitLog Insights for QA is a lightweight tool designed to provide QA teams with actionable insights extracted from Git commit history. By analyzing such data, testing teams can make informed decisions, improve testing approaches, and streamline their testing processes. The framework provides utility functions to extract and visualize data from Git logs, such as contributors, files, commits, pull requests, etc. To extract the data, it uses PyDriller, a Python framework for mining software repositories, and GitHub API.

## Insights

This project provides some utility functions that can generate insights from the data. These insights can help understand the patterns and trends in the GitHub repositories data and how they can help the testing team. Some of the insights are:

### Top Touched files

Find the top files that have been modified the most in a given time period.

Possible inferences:
Focus testing efforts on files that have undergone frequent changes and are complex.

Encourages testers to focus on complex files and consider collaborating with the primary authors for in-depth testing, highlighting the importance of prioritizing testing efforts effectively.

Resource allocation - Allocate more resources for files that underwent considerable modifications
Ownership and expertise - Identify developers who are authors of important files
Complexity and testing focus - Assess the complexity of files and align testing efforts accordingly
Collaboration with developers - Know which authors to collaborate with for which modules


### PR Review time

### Merge Activity

### Author Bias

### Size of PRs


## Installation
To install gitlog-insights, you need to have Python 3.10 or higher and pip installed on your system. You also need to install PyDriller and its dependencies. 

1. Clone this repository:
   ```sh
   git clone https://github.com/qxf2/gitlog-insights.git
   cd gitlog-insights

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt

## Usage
To use gitlog-qa-insights, you need to provide the path to the Git repository that you want to analyze, and optionally the start and end dates for the analysis. You can use any of the utility functions provided in the helpers folder to get the data and insights that you need. 

1. To access the GitHub API, you would need a personal access token. For information on how to create a personal access token, see "Creating a personal access token". Once created, export using: 
```
export TOKEN=
```

2. The scripts that generate insights are present in the insights folder. You can run any of the insights by using the corresponding script and providing the required arguments.
   ```
   python insights/get_most_touched_files.py
   ```
   You can find more details in the respective script.
   

## Examples



## License
This project is licensed under the MIT License.
