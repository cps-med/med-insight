# med-insight

**Med-Insight** is an AI-powered, full-stack healthcare analytics application designed to help providers deliver safer, higher-quality care by transforming complex patient treatment data into actionable insights. The platform enables clinicians to assess outcomes, identify best practices, and monitor the effectiveness of care delivery across diverse treatment settings.

Built as an end-to-end solution, Med-Insight integrates data from multiple clinical systems, performs ETL processing into a structured database or data warehouse, and applies advanced AI/ML techniques to uncover patterns, trends, and recommendations that support data-informed decision making at the point of care. The end-user interface provides a dashboard for top-level insights data exploration.

The complete Med-Insight application consists of three subsystems, organized as subdirectories under the the parent _med-insight_ folder. These subsystems/components consist of:

* **med-data:** Mock data sources for med-insight development and testing
* **med-etl:** ETL functionality to retreive, process, and store data in a data mart
* **med-ml:** AI and Machine learning layer
* **med-view:** Web UI for medical data analysis, reporting, and visualization

## Getting Started
#### Clone the Repository
To get started, clone the med-insight repository into a directory of your choice. For example, `~/swdev/med/`.

```txt
git clone https://github.com/cps-med/med-insight.git  
```

This will create the root med-insight folder and subfolders for each of the three subsystems.  

#### Create Folder Structure for Extract and Logging Files
In addition to the med-insight application, you will need to create a location for the extract and logging files. This location is configurable, but assumed to be adjacent to med-insight. Create the base med-output folder and two subfolders.  

Note that this folder and subfolders are **not** managed via source control.

```text
cd <parent folder for med-insight and med-output>
mkdir -p med-output/extract
mkdir -p med-output/log
```

Your directory structure should look like:

```text
.                      # parent folder for application and output files
├── med-insight        # med-insight application (under git version control)
│   ├── med-data       # subsystem for mock data
│   ├── med-etl        # subsystem for etl processing
│   ├── med-ml         # subsystem for ai/ml processing
│   ├── med-view       # subsystem for web app
└── med-output         # base location for output files (not under version control)
    ├── extract        # clinical data extract files
    └── log            # med-etl and med-view application logs
```

## Claude Code
The med-insight development project uses Claude Code as an AI assistant. For simplicity, all Claude activity and supporting markdown files are located in the root project directory (as opposed to scattered throughout project subfolders).  

Install Claude Code on your local development machine via either of the terminal commands below.  
My preference is the first option (Homebrew).  
```bash
brew install --cask claude-code
-or-
curl -fsSL https://claude.ai/install.sh | bash
```

Once installed, cd to your project and run:  

```bash
claude
```

## Local Environment Setup
Refer to the README.md files in each of the three subsystems for information on the respective tech stack, local development environment setup, and general guidance. You may need to reach out to a peer developer to get secret and sensitive information that is not under version control, such as the contents of .env files.

## GitHub Issues
GitHub Issues is used to track and manage development work across all three subsystems in a lightweight but structured manner. Each issue represents a coding task and should include relevant context and status updates. Once a task is complete, it can be closed with a comment.
