# Python Poetry

Installation Guide and Django Dependency Management

---

# Table of Contents

- [1 Poetry](#1-poetry)
- [2 Poetry](#2-poetry)
- [3 System Requirements](#3-system-requirements)
- [ 4 Installation](#4-installation)
  - [4.1 Install Poetry on macOS/Linux ](#41-install-poetry-on-macoslinux)
  - [4.2 Add Poetry to your System Path (Linux or Mac)](#42-add-poetry-to-your-system-path-linux-or-mac)
  - [4.3 Verify Installation (Linux or Mac)](#43-verify-installation-linux-or-mac)
  - [4.4 Install Poetry on Windows](#44-install-poetry-on-windows)
- [5 Project Setup](#5-project-setup)
  - [5.1 Initialized Project](#51-initialized-project)
  - [5.2 Generated pyproject.toml File](#52-generated-pyprojecttoml-file)
  - [5.3 Poetry Install](#53-poetry-install)
  - [5.4 Django Project With Poetry](#54-django-project-with-poetry)
- [6 Manage Project](#6-manage-project)
  - [6.1 Poetry Add Package](#61-poetry-add-package)
  - [6.2 Poetry Update Package](#62-poetry-update-package)
  - [6.3 Poetry Remove Installed Package](#63-poetry-remove-installed-package)
  - [6.4 Poetry Show Installed Package](#64-poetry-show-installed-package)
  - [6.6 Poetry Run Command](#66-poetry-run-command)
  - [6.7 Poetry Shell Command](#67-poetry-shell-command)
  - [6.8 Poetry Export](#68-poetry-export)
- 7 [Poetry Self](#7-poetry-self)
  - [7.1 Poetry Self Update](#71-poetry-self-update)
  - [7.2 Poetry Self Add](#72-poetry-self-add)
  - [7.3 Poetry Self Remove](#73-poetry-self-remove)
  - [7.4 Poetry Self Show](#74-poetry-self-show)
  - [7.5 poetry self lock](#75-poetry-self-lock)
  - [7.6 Poetry Self Install](#76-poetry-self-install)

## 1 Poetry

Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. Poetry offers a lockfile to ensure repeatable installs, and can build your project for distribution.

## 2 Why Poetry

**Compatibility between versions** : A good thing about using poetry is the compatibility check between versions. Suppose you’re using pandas 1.0 with numpy 1.19 and it works fine. If numpy updates to a newer version that is not compatible with pandas 1.0 we could have a problem there. But when you run poetry update , all the compatibility tables are checked before changing to newer version. This really helps preventing errors.

Poetry offers a more user-friendly approach and it simplifies the process of managing dependencies and projects. Poetry replaces the need for multiple files like setup.py, requirements.txt, setup.cfg, and Pipfile, making dependency management and package building more straightforward.

**Better Resolver**: Poetry has a more advanced dependency resolution, so it can handle conflicts more effectively and does not lead to issues in version pinning. Poetry employs a straightforward `pyproject.toml` file to handle packages and projects as opposed to dealing with complicated configuration files or individually defining each package and version.

**Dependency Management**: Pip requires some manual configuration to use at maximum efficiency. Poetry aims to dispel this and be more user-friendly so that the common tasks will be more simple.

**Dependency Specification**: Poetry allows for precise dependency specification, including version constraints, and supports both development and production dependencies.

**Integration with Other Tools**: Poetry can work well with other tools and services, including CI/CD pipelines and Docker.

## 3 System Requirements

Poetry requires Python 3.8+. It is multi-platform and the goal is to make it work equally well on Linux, macOS and Windows.

## 4 Installation

### 4.1 Install Poetry on macOS/Linux

Open your terminal. Run the following command to install Poetry:

```zsh
curl -sSL https://install.python-poetry.org | python3 -

```

### 4.2 Add Poetry to your System Path (Linux or Mac):

Add Poetry to your system's `PATH` by adding the following line to your shell configuration file (`~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`):

```zsh
export PATH="$HOME/.local/bin:$PATH"
```

Reload your shell configuration:

```zsh
source ~/.bashrc  # or source ~/.zshrc
```

### 4.3 Verify Installation (Linux or Mac)

```zsh
poetry --version
```

### 4.4 Install Poetry on Windows

Open PowerShell Run the following command to install Poetry:

```zsh
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Add Poetry to your system's PATH by running:

```zsh
setx PATH "%USERPROFILE%\.local\bin;%PATH%"
```

Close and reopen PowerShell.
Verify the installation:

```zsh
poetry --version
```

## 5 Project Setup

The poetry `init` command is used to create a `pyproject.toml` file interactively. This file is the heart of a Poetry-managed project, containing metadata, dependencies, and configuration for your Python package. The command guides you through the process of setting up your project by prompting you for essential information.

### 5.1 Initialized Project

o initialize a new Poetry project, run the following command in your terminal:

```zsh
poetry init
```

This will start an interactive session where you will be prompted to provide details about your project.

**Interactive Prompts**:
If you run poetry init without any options, Poetry will guide you through the setup process interactively. Below is an example of the prompts you will encounter:

```zsh
poetry init \
  --name my_package \
  --description "A sample Python package" \
  --author "John Doe <john.doe@example.com>" \
  --dependency requests:^2.25.1 \
  --dev-dependency pytest:^6.2.0
```

This will generate a `pyproject.toml` file with the specified configuration.

**Options**:
The poetry init command supports several options to customize the initialization process. Below is a detailed explanation of the available options:

`--name` Specifies the name of your package. The name should be unique and follow Python package naming conventions (lowercase, underscores allowed).

```zsh
poetry init --name my_package_name
```

`--description` Provides a short description of your package. This description will be included in the `pyproject.toml` file and used in package metadata.

```zsh
poetry init --description "A short description of my package"
```

`--author` Specifies the author of the package. The author field typically includes the author's name and email address.

```zsh
poetry init --author "John Doe <john.doe@example.com>"
```

`--dependency` Adds a package dependency with a version constraint.You can specify multiple dependencies by repeating the --dependency option. The version constraint follows the format package_name:version_specifier (e.g., `requests:^2.25.1`).

```zsh
poetry init --dependency requests:^2.25.1
```

`--dev-dependency` Adds a development dependency with a version constraint. Development dependencies are used for tools and libraries required during development (e.g., `testing frameworks`, `linters`).You can specify multiple development dependencies by repeating the `--dev-dependency` option.

```
poetry init --dev-dependency pytest:^6.2.0
```

### 5.2 Generated pyproject.toml File

After running poetry init, a pyproject.toml file will be created in your project directory. Here’s an example of what it might look like:

```
[tool.poetry]
name = "my_package"
version = "0.1.0"
description = "A sample Python package"
authors = ["John Doe <john.doe@example.com>"]
license = "MIT"

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.25.1"

[tool.poetry.dev-dependencies]
pytest = "^6.2.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

### 5.3 Poetry Install

The `poetry install` command is used to install the dependencies specified in your project's `pyproject.toml` file. It resolves the dependencies, creates or updates the `poetry.lock` file, and installs the packages into the project's virtual environment.

To install dependencies for your project, run the following command in your terminal:

```zsh
poetry install
```

**How It Works**:

- **Reads `pyproject.toml`:** Poetry reads the `pyproject.toml` file to determine the dependencies and their version constraints.

- **Resolves Dependencies:** Poetry resolves the dependencies to find compatible versions of all packages. If a `poetry.lock` file exists, Poetry uses the exact versions specified in it to ensure consistency.

- **Creates or Updates `poetry.lock`:** If there is no poetry.lock file, Poetry creates one after resolving dependencies. If a poetry.lock file exists, Poetry updates it if necessary.

- **Installs Dependencies:** Poetry installs the resolved dependencies into the project's virtual environment.

**Options:**

The `poetry install` command supports several options to customize the installation process. Below is a detailed explanation of the available options:

1. `--without` Excludes one or more dependency groups from the installation.

   ```zsh
   poetry install --without <group1>,<group2>
   ```

   Dependency groups are defined in the `pyproject.toml` file under `tool.poetry.group`. For example, if you have a dev group for development dependencies, you can exclude it using:

   ```zsh
   poetry install --without dev
   ```

   Multiple groups can be excluded by separating them with commas:

   ```zsh
   poetry install --without dev,test
   ```

2. `--with` Includes one or more optional dependency groups in the installation.

   ```zsh
   poetry install --with <group1>,<group2>
   ```

   This option is useful for including optional groups that are not installed by default.For example, if you have an optional docs group, you can include it using:

   ```zsh
   poetry install --with docs
   ```

3. `--no-dev` Excludes development dependencies from the installation.

   ```zsh
   poetry install --no-dev
   ```

   This option is equivalent to `--without dev`.It is commonly used in production environments to avoid installing unnecessary development tools.

4. `--sync` Synchronizes the virtual environment with the `poetry.lock ` file by removing unused dependencies.

   ```zsh
   poetry install --sync
   ```

   This option ensures that the virtual environment matches the exact state defined in the `poetry.lock` file. It removes any packages that are not in the `poetry.lock` file.

5. `--dry-run` Displays the operations that would be performed without actually executing them.

   ```zsh
   poetry install --dry-run
   ```

   This option is useful for debugging or verifying the installation process.

**Examples**

1. **Install All Dependencies** To install all dependencies (including development dependencies):

   ```zsh
   poetry install
   ```

2. **Exclude Development Dependencies** To install only production dependencies (exclude development dependencies):

   ```zsh
   poetry install --no-dev
   ```

3. **Exclude Specific Dependency Groups** To exclude specific dependency groups (e.g., `dev` and `test`):

   ```zsh
   poetry install --without dev,test
   ```

4. **Include Optional Dependency Groups** To include optional dependency groups (e.g., `docs`):

   ```zsh
   poetry install --with docs
   ```

5. **Synchronize the Virtual Environment** To synchronize the virtual environment with the `poetry.lock` file:

   ```zsh
   poetry install --sync
   ```

6. **Dry Run** To preview the installation process without making changes:

   ```zsh
   poetry install --dry-run
   ```

## 6 Manage Project

### 6.1 Poetry Add Package

The `poetry add` command is used to add new dependencies to your project. It updates the `pyproject.toml` file with the specified package and installs it into the project's virtual environment. If no version constraint is provided, Poetry automatically selects a suitable version based on the latest available releases.

To add a package to your project, run the following command in your terminal:

```zsh
poetry add <package_name>
```

For example, to add Django:

```zsh
poetry add django
```

**How It Works:**

- **Adds the Package to `pyproject.toml`:** Poetry adds the package and its version constraint to the `[tool.poetry.dependencies]` section of the `pyproject.toml` file.

- **Resolves Dependencies:** Poetry resolves the dependencies to ensure compatibility with the existing packages in your project.

- **Installs the Package:** Poetry installs the package and its dependencies into the project's virtual environment.

- **Updates poetry.lock:** Poetry updates the `poetry.lock` file to reflect the exact versions of the installed packages.

**Options:**<br>
The poetry add command supports several options to customize the installation process. Below is a detailed explanation of the available options:

1. **Version Constraints:** Specifies the version constraint for the package.

   ```zsh
   poetry add <package_name>@<version_constraint>| poetry add django@5.0.6
   ```

2. `--dev` Adds the package as a development dependency.

   ```zsh
   poetry add <package_name> --dev | poetry add pytest --dev
   ```

   The package will be added to the [tool.poetry.dev-dependencies] section of the pyproject.toml file.

3. `--optional` Adds the package as an optional dependency.

   ```zsh
   poetry add <package_name> --optional
   ```

   The package will be added to the `[tool.poetry.extras]` section of the `pyproject.toml` file. Optional dependencies are not installed by default and must be explicitly included during installation.

4. `--allow-prereleases` Allows the installation of pre-release versions of the package.

   ```zsh
   poetry add <package_name> --allow-prereleases
   ```

   This option is useful if you want to install alpha, beta, or release candidate versions of a package.

### 5.4 Django Project With Poetry
1. **Create Project Directory**

   ```zsh
   mkdir my_django_project
   cd my_django_project
   ```

2. **Initialize Poetry**

   ```zsh
   poetry init
   ```
3. **Adding Django to the Project**

   ```zsh
   poetry add django
   ```
4. **For REST APIs:**

   ```zsh
   poetry add djangorestframework
   ```
5. **Development tools:**

   ```zsh
   poetry add --group dev black ruff pytest pytest-django
   ```
 6. **Creating Django Project**
      ```zsh
      poetry run django-admin startproject config .
      ```
 7. **Run Server**

      ```zsh
      poetry run python manage.py runserver 0.0.0.0:8000
      ```
8. **Run Django Commands**
   ```zsh
   poetry run python manage.py makemigrations
   poetry run python manage.py migrate
   poetry run python manage.py createsuperuser
   poetry run python manage.py collectstatic
   ```
9. **Add Packages to Poetry**

   ```zsh
   poetry add redis celery
   ```
10. **Remove Packages from Poetry**

    ```zsh
    poetry remove redis
    ```
11. **Update Dependencies**
    ```zsh
    poetry update
    ```
12. **Show Installed Packages**
    ```zsh
    poetry show
    ```
13. **Poetry with Multiple Environments**
    ```zsh
    poetry add gunicorn --group prod
    poetry add django-debug-toolbar --group dev
    ```

### 6.2 Poetry Update Package

The poetry update command is used to update the dependencies in your project to their latest versions, based on the constraints specified in the `pyproject.toml` file. It resolves the dependencies, updates the `poetry.lock` file, and installs the latest compatible versions of the packages.

To update all dependencies in your project, run the following command in your terminal:

```zsh
poetry update
```

poetry update <package_name1> <package_name2>

```zsh
poetry update <package_name1> <package_name2> | poetry update django pytest
```

Output:

```
$ poetry update
Updating dependencies
Resolving dependencies... (0.5s)

Package operations: 2 installs, 3 updates, 0 removals

  - Updating django (5.0.6 -> 5.1.0)
  - Updating requests (2.25.1 -> 2.26.0)
  - Installing new-package (1.0.0)
  - Installing another-package (2.0.0)

Writing lock file
```

### 6.3 Poetry Remove Installed Package

The `poetry remove` command is used to uninstall and remove a package from your project. It updates the pyproject.toml file and removes the package from the virtual environment.

To remove a package, run the following command in your terminal:

```zsh
poetry remove <package_name> | poetry remove requests
```

**Output Example:**

```
$ poetry remove requests
Removing requests (2.26.0)

Updating dependencies
Resolving dependencies... (0.3s)

Writing lock file
```

### 6.4 Poetry Show Installed Package

The poetry show command lists all the installed packages in your project, along with their versions and descriptions.

To list all installed packages, run the following command in your terminal:

```zsh
poetry show
```

**Options:**

- `--tree` Displays the dependency tree.

  ```zsh
  poetry show --tree
  ```

- `--latest` Shows the latest version of each package.

  ```zsh
  poetry show --latest
  ```

- `--outdated` Lists only packages that are outdated.
  ```zsh
  poetry show --outdated
  ```
  **Example Output:**

```
$ poetry show
asgiref     3.8.1  ASGI specs, helper code, and adapters
django      5.1.0  A high-level Python web framework
requests    2.26.0 Python HTTP for Humans.
```

### 6.5 Poetry Check Command

The poetry check command validates the `pyproject.toml` file and ensures its consistency with the `poetry.lock` file. It checks for errors and provides a detailed report if any issues are found.

To validate your project configuration, run the following command in your terminal:

```zsh
poetry check
```

**Example Output:**
When you run `poetry check`, you may see output similar to the following:

```
$ poetry check
All set!
```

If there are errors, the output might look like this:

```
$ poetry check
Error: Invalid TOML file in pyproject.toml
```

### 6.6 Poetry Run Command

The poetry run command executes a given command inside the project's virtual environment. This ensures that the command has access to all the dependencies installed in the virtual environment.

To execute a command inside the virtual environment, use the following syntax:

```zsh
poetry run <command>
```

**Examples:**

- **Run a Python Script:** To run a Python script (e.g., manage.py for Django):

  ```zsh
  poetry run python manage.py runserver
  ```

- **Run a CLI Tool:** To run a command-line tool installed in the virtual environment (e.g., pytest):

  ```zsh
  poetry run pytest
  ```

- **Run a Custom Script:** To run a custom script defined in your pyproject.toml file:

  ```zsh
  poetry run my_script
  ```

### 6.7 Poetry Shell Command

The poetry shell command spawns a new shell session within the project's virtual environment. If a virtual environment does not exist, Poetry will create one.

To activate the virtual environment in a new shell, run:

```zsg
poetry shell

```

**Example:**

To work interactively in the virtual environment:

```
poetry shell
# Now you're inside the virtual environment
python manage.py runserver
pytest
exit  # Exit the virtual environment shell
```

### 6.8 Poetry Export

This command exports the lock file to other formats, making it easier to share dependencies in a format compatible with other package managers like pip.

To export the dependencies to a requirements.txt file:

```zsh
poetry export -f requirements.txt --output requirements.txt
```

If you want to export the dependencies without including hashes:

```zsh
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

## 7 Poetry Self

The `poetry self` command is used to manage the Poetry installation itself. It provides subcommands to update Poetry, manage its dependencies, and interact with its internal configuration. Below is a detailed documentation of the poetry self command and its subcommands.

```zsh
poetry self [options] <command>
```

### 7.1 Poetry Self Update

`poetry self update` Updates Poetry to the latest version.

```zsh
poetry self update [options]
```

Update Poetry to the latest stable version:

```zsh
poetry self update
```

Update Poetry to a specific version:

```zsh
poetry self update --version 1.2.0
```

poetry self update --preview

```zsh
poetry self update --preview
```

### 7.2 Poetry Self Add

Adds a dependency to Poetry's own environment. This is useful for extending Poetry with plugins or additional tools.

```zsh
poetry self add <package> [options]
```

**options:**

`--editable`: Install the package in editable mode.

`--extras` <extras>: Install additional features of the package.

`--source` <source>: Specify a custom source for the package.

Add a package to Poetry's environment:

```zsh
poetry self add black
```

Add a package in editable mode:

```zsh
poetry self add --editable ./my-plugin
```

### 7.3 Poetry Self Remove

Removes a dependency from Poetry's environment.

```zsg
poetry self remove <package> | poetry self remove black
```

### 7.4 Poetry Self Show

Displays information about Poetry's environment, including installed packages and their versions.

```zsh
poetry self show [options] | poetry self show | poetry self show --tree
```

`--tree`: Display dependencies as a tree.

`--latest`: Show the latest version of each package.

`--outdated`: Show only outdated packages.

### 7.5 poetry self lock

Creates a poetry.lock file for Poetry's own dependencies. This is useful for ensuring reproducibility when extending Poetry with plugins.

```zsh
poetry self lock
```

### 7.6 Poetry Self Install

Installs Poetry's dependencies based on the poetry.lock file.

Install Poetry's dependencies:

```zsh
Install Poetry's dependencies:
```

Synchronize Poetry's environment:

```zsh
poetry self install --sync
```
