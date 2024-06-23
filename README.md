# Gitkeepr

Gitkeepr is a powerful and user-friendly command-line interface (CLI) tool designed to help you manage your Github repositories efficiently.

## Features

With Gitkeepr, you can...

- Create repositories: Create new GitHub repositories effortlessly.
- List repositories: List all repositories of a specified GitHub user.
- Clone repositories: Clone repositories to your local machine.
- Manage collaborators: Add or remove collaborators from your repositories.

## Installation

Gitkeepr can be installed using Poetry. Ensure you have Poetry installed on your system.

1. Clone the repository

   ```shell
   git clone https://github.com/yourusername/gitkeepr.git
   cd gitkeepr
   ```

2. Install dependencies

   ```shell
   poetry install
   ```

3. Set up your environment variables for GitHub API

   ```bash
   export GITHUB_USERNAME="your username"
   export GITHUB_API_TOKEN="my-token"
   ```

## Usage

You can use Gitkeepr directly through the command line.

```shell
gitkeepr --help
```
