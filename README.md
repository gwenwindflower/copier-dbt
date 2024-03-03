# 📝🖨️ copier-dbt 🧡⚙️

This is a [copier](https://github.com/copier-org/copier) template for [dbt](https://getdbt.com) projects. It's useful for scaffolding out a basic project structure and configuration with modern tooling quickly.

> [!NOTE]
> This is a very new project. It's so far only been tested using MacOS with BigQuery, DuckDB, and Snowflake. For it to become robust, it needs to be tested on other platforms and with other data warehouses. I very much welcome Issues, Discussions, and Pull Requests to help make this project better. Even if you're not comfortable contributing code, testing it out with various platforms and warehouses and reporting any issues you encounter is _incredibly_ helpful. When we get further along I'll create a support matrix with platform and warehouse coverage detailed.

You will need `python3`, [`pipx`](https://github.com/pypa/pipx), and `git` installed to use this template. You will also need a database to connect to. If you don't want have or want access to a cloud warehouse I suggest using DuckDB, which runs locally and thus is simpler to connect to.

## Table of contents

- [Features](#features)
- [Non-goals](#non-goals)
- [Usage](#usage)
- [Tips](#tips)

## Features

The following features are implemented or planned:

- [x] dbt [Best Practices project structure](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview)
- [x] Basic initial dbt Project configuration
- [ ] Coverage of all non-password-based authentication methods for the below warehouses[^1]
- [ ] Warehouse-aware dbt profile configuration for the following options, check out the [dbt docs on warehouse-specific profile configs](https://docs.getdbt.com/docs/core/connect-data-platform/about-core-connections) for more details:
  - [x] Snowflake - using `authenticator: externalbrowser` with SSO
  - [x] BigQuery - using `method: oauth` via `gcloud` CLI
  - [ ] Databricks - using `token: <empty>`, you will need to create a personal access token in Databricks, and fill it into that field in to your `~/.dbt/profiles.yml` manually once the project is created[^1]
  - [ ] Redshift - using `method: IAM` via `awscli`
  - [ ] Postgres - still haven't decided the best way to handle Postgres
  - [x] DuckDB - local warehouse, no authentication required
- [x] Linting and formatting of SQL with SQLFluff
- [x] Configurable linting rules in the setup process
- [ ] Use `sqlfmt` instead of `SQLFluff` for formatting
- [ ] Option to not use a SQL linter or formatter
- [x] Modern Python tooling from astral.sh: `ruff` and `uv` for formatting, linting, and dependency management
- [x] Pre-commit hooks for automated linting, formatting, and fixes on commit
- [ ] Selection of various pre-commit hooks or not using pre-commit at all
- [x] A selection of recommended dbt packages:
  - `dbt-utils`
  - `dbt-expectations`
  - `dbt-date`
  - `dbtplyr`
  - `dbt-codgen`
- [ ] A selection of useful macros relevant to most projects (e.g. `limit_in_dev`, `cents_to_dollars`, etc.)
- [ ] `dbt-codegen` scripts to build sources and staging models from warehouse metadata on project creation
- [ ] Support for generating a new [dbt Cloud](https://cloud.getdbt.com/) project and setting up the dbt Cloud CLI instead of a `profiles.yml` file
- [ ] CI/CD configurations for various major git hosting services (GitHub Actions, GitLab CI, Bitbucket Pipelines, etc.)

### Non-goals

These are the things at present I don't plan on implementing. I'm quite open to changing my mind on these, but I have reasons for not including them right now which are listed below.

- A selection of models and tests for common use cases:
  - You should use dbt packages on the dbt Package Hub for this. We don't want to reinvent the wheel here. This one probably won't change.
- Password-based authentication for warehouses:
  - We move the profiles.yml out of the project on template creation, so credentials are never stored or committed to the repo created from this template. Thus, while highly unlikely that this would be a security risk, I just don't feel comfortable supporting it for the time being. I'm very open to hearing from more experienced database security professionals on differing opinions, or any ideas on how to leverage something like environment variables for increased security while still providing a good developer experience. That said, I want to complete the main goals of this project before tackling this.
- Using `pip` instead of `uv`:
  - `uv` is a _much_ faster and more modern tool for Python package management, and I'd like to encourage its adoption. While I want to provide as much optionality as possible, changing this would be more complicated and I decided to make a choice — that said you're more than welcome to fork this repo and change it to use `pip` if you'd like! Like the rest of the non-goals, once I've accomplished the main goals I'm open to revisiting this.
- All of the above re `uv` for `ruff` as well. The [astral.sh](https://astral.sh/) tooling is just really great, handles the job of multiple tools in one, and is so fast, I don't think I can be persuaded to go backwards on this one. Now if only somebody would make `ruff` for SQL...

## Usage

Before embarking on this quick journey: if your data platform has a CLI tool that lets you authenticate, like `gcloud` for BigQuery, `awscli` for Redshift, etc., make sure you have it installed and authenticated before running the setup process, as we will use these tools to authenticate and configure your `~/.dbt/profiles.yml` file in the most simple and secure way possible.[^1]

1. Install `copier` if you haven't already:

   ```shell
     pipx install copier
   ```

   - pipx is like pip, but for installing global Python CLI tools
   - It houses each tool in a dedicated virtual environment, so you don't have to worry about dependency conflicts

2. Create a new dbt project from this template:

   ```shell
   copier gh:gwenwindflower/copier-dbt <path/to/project_name> --trust
   ```

   - `gh:` tells copier to use a GitHub repository as the source for the template
   - The directory you specify is where the new project will be created, don't create it beforehand
   - `copier` will run a series of commands to set up your project after it templates everything. These are listed in the `copier.yml` at the bottom in the `_tasks` list. I highly encourage you to look through these before and make sure you really do trust and understand them before using the `--trust` flag above that will allow them to run. These commands are very straightforward and standard, but letting somebody's code run commands on your machine should always be taken seriously. In brief they will do the following (but seriously go look at the file):
     - Create and activate a virtual environment for the project in your newly templated project directory
     - Install the project's dependencies
     - Put the contents of the `profiles.yml` file in the correct place in your home directory then remove the file from your project for security
     - Initialize a new git repo in your project and make an initial commit
     - Install the pre-commit hooks in your project
     - If you feel more comfortable with it, you can delete the tasks section, skip the `--trust` flag, and run the commands manually after the project is created

3. Follow the prompts to configure your project, depending on your answers to certain prompts, different prompts may appear or disappear (e.g. if you choose your `data_warehouse` as `bigquery` you'll get a different set of questions to configure the `profiles.yml`).

4. Your project is now ready to use! `cd` into the newly created project and run:

   ```shell
   dbt deps
   dbt debug
   ```

   - `dbt deps` will install the dbt packages included in the template
   - `dbt debug` will run a series of tests to ensure that your dbt project is configured correctly and connects to your data warehouse properly

5. Start building your dbt project!

- Consider using the included `dbt-codegen` package to build some initial sources and staging models from your data warehouse metadata.
- Once you've got some models built, try running `dbt build` to run and test your models.

6. Commit it!

- The setup process will have initialized a git repository for you and made an initial commit of the starting state, so you can go right ahead and push your new project to your favorite git hosting service. It will run the pre-commit hooks automatically on commit, so you don't have to worry about linting or formatting your code before you commit it.

## Tips

- If you're looking to just explore dbt, try using some of the public datasets potentially available on your platform. Most have a lot of cool ones! For example, BigQuery has a public dataset for the New York City Taxi and Limousine Commission that's really fun to play with. If you use DuckDB and connect to MotherDuck they have a bunch of Hacker News data that's quite fun to play with.

- This project, thanks to the incredible `uv` and it's native support of `pip-tools`' `pip compile` functionality, uses a more readable `requirements.in` file to define top-level dependencies, which then compiles that to a highly detailed `requirements.txt` file which maps all sub-dependencies to the top-level packages they are required by. This makes it much easier to deal with versions and upgrading. Also `uv `is wildly fast. Take a peek at these files to get the gist, and check out [`uv`'s documentation](https://github.com/astral-sh/uv) to learn more.

- If you decide you like `uv`, it may be a good idea to install it globally so you can use it for initializing new projects and other things. You can find the installation instructions in the [ `uv` documentation ](https://github.com/astral-sh/uv).

- Always make sure you're installing Python packages in a virtual environment to avoid dependency conflicts(or using `pipx` if it really is supposed to be global). Not to be a broken record, but _yet another_ cool thing `uv` does is always install your packages into a virtual environment by default, even if it's not activated (unlike `pip`), and it will prompt you to create one if one doesn't exist yet. This comes in _super_ handy to save you from accidentally installing a project's dependencies globally.

  - If you need to update any dependencies you can change the version(s) in the `requirements.in` file and run `uv pip compile requirements.in -o requirements.txt` to compile an updated `requirements.txt` file. Then run `uv pip install -r requirements.txt` to install the updated dependencies.

- If you don't want use a cloud warehouse, I recommend using `duckdb` as your local warehouse. It's a really neat database that's super fast on medium-sized data and has one of the best SQL syntaxes in the game right now. It can run completely locally, but you can also easily wire it up to cloud storage like S3 or GCS, or even a cloud warehouse SaaS called [MotherDuck](https://motherduck.com/).

- Typing long commands is a bummer, if you plan on doing a lot of Python and dbt development, I highly recommend setting up _*aliases*_ for common commands in your shell configuration (`~/.bashrc`, `~/.zshrc`, etc.). For example, you could add the following to your shell configuration to make running dbt and python commands easier (just make sure they don't conflict with existing aliases or commands, customize to your liking!):
  ```shell
  export EDITOR=<your favorite text editor>
  # dbt alias suggestions
  alias dbtp="$EDITOR ~/.dbt/profiles.yml"
  alias db="dbt build"
  alias dbs="dbt build -s"
  alias dt="dbt test"
  alias dts="dbt test -s"
  alias dr="dbt run"
  alias drs="dbt run -s"
  alias dp="dbt parse"
  alias dmv="dbt parse && mf validate-configs"
  # Python alias suggestions
  alias python="python3"
  alias venv="uv venv .venv"
  alias va="source .venv/bin/activate"
  alias venva="venv && va"
  alias pi="uv pip"
  alias pir="uv pip install -r"
  alias pirr="uv pip install -r requirements.txt"
  alias pc="uv pip compile requirements.in -o requirements.txt"
  alias piup="uv pip install --upgrade pip"
  alias vpi="venva && piup && pirr"
  alias vpci="venva && piup && pc && pirr"
  # Go-to your project, activate the virtual environment, and open it in your text editor
  alias <something short and memorable>="cd <path to your project> && venva && $EDITOR ."
  ```
  - Notice we can use previously defined aliases in new aliases. For example, `vpci` uses `venva` and `pirr` to update the project's dependencies and install them.

[^1]: I've only selected the most secure and simple authentication method for each warehouse for the time being. You can manually configure more complex and specific authentication methods like password-based authentication, SSO, JSON keys, etc. in the `~/.dbt/profiles.yml` file after the setup process is complete. Wherever possible though, I've opted for _simplicity_ and _security_ — for example the configuration for BigQuery requires that you have installed the `gcloud` CLI and authenticated using OAuth through that. The Redshift authentication method is also the most secure and simple method available, using IAM roles and the `awscli`'s `~/.aws/config` credentials to authenticate. I highly recommend sticking with these methods and using these tools if it's an option.
