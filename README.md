# News Summarizer

## Overview

The News Summarizer is a Python-based tool that scrapes articles from leading tech news websites and provides concise summaries using the ChatGPT API. The script currently fetches articles related to the search term "AI" from the following sources:
- **Tech Crunch**
- **FirstPost**
- **The Verge**
- **Business Insider**
- **ArsTechnica**
- **Wired**

## Features

- **Automated Article Retrieval**: Scrapes the latest articles from top tech news websites based on a specific search term.
- **AI-Powered Summaries**: Leverages the ChatGPT API to generate concise, 5-sentence summaries for each article.
- **Daily Updates**: Uses GitHub Actions to run the script daily, ensuring you receive the latest tech news directly to your inbox.
- **Email Notifications**: The summarized news is emailed to a designated mailing list, keeping you up to date with minimal effort.

## How It Works

1. The script scrapes articles from the specified websites based on the given search term ("AI" by default).
2. The articles are then processed by the ChatGPT API to generate short summaries.
3. GitHub Actions runs the script daily and emails the summarized news to the specified recipients.

## Requirements

- Python 3.9
- Selenium
- ChatGPT API Key, and library
- GitHub account with Actions enabled

## Setup

1. Clone the repository.
2. Set up your ChatGPT API key in the environment secrets.
3. Configure your GitHub Actions workflow to run the script daily.
4. Add email recipients to the mailing list.
