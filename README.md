# ADR-py

> Shout to excellent [adr-tools](https://github.com/npryce/adr-tools) project on which `ADR-py` is based on

This Python script is designed to help software development teams document their architecture decisions using Architecture Decision Records (ADRs). 
ADRs are a lightweight and effective way to capture important decisions made during the design and development of a software system, and to keep track of their rationale and implications over time.

The script creates ADR files in a predefined format, following the principles of **[Michael Nygard's ADR template](https://github.com/joelparkerhenderson/architecture-decision-record/tree/main/locales/en/templates/decision-record-template-by-michael-nygard)**. 
Each ADR file is a Markdown document with a unique name that includes a sequential number and a title, which is automatically generated based on the information provided by the user.

## Prerequisites

- Python 3.11 installed on your system.
- Basic knowledge of command-line interface (CLI) usage.

## Installation

- `pip install adr`

## How to Use

**Usage**:

```console
$ adr [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `init`: Initialize ADR directory with first ADR in given PATH
* `new`: Create new ADR with given NAME

## `init`

Initialize ADR directory with first ADR in given PATH

**Usage**:

```console
$ adr init [OPTIONS] [PATH]
```

**Arguments**:

* `[PATH]`: Path in where ADRs should reside. If not provided Path will be extracted from pyproject.toml

**Options**:

* `--help`: Show this message and exit.

## `new`

Create new ADR with given NAME

**Usage**:

```console
$ adr new [OPTIONS] NAME
```

**Arguments**:

* `NAME`: Name of new ADR. Longer names (with spaces) should be put in quotation marks.  [required]

**Options**:

* `adr --help`: Show this message and exit.


## **ADR Template**

The generated ADR files follow the template proposed by Michael Nygard in his book "Documenting Architecture Decisions." The template consists of the following sections:

- Title: The title of the ADR.
- Status: The current status of the decision (e.g., proposed, accepted, rejected).
- Context: The context and background information that led to the decision.
- Decision: The decision made and its rationale.
- Consequences: The potential consequences and trade-offs of the decision.

## **Benefits of ADRs**

Using ADRs has several benefits for software development teams, including:

- Documentation: ADRs provide a written record of important architectural decisions, making it easier for team members to understand the reasons behind past decisions.
- Communication: ADRs serve as a communication tool for discussing and documenting design decisions, facilitating collaboration among team members.
- Decision-making: ADRs encourage thoughtful decision-making by requiring the team to consider the context, rationale, and potential consequences of each decision.
- Transparency: ADRs promote transparency by making architectural decisions visible and accessible to the entire team, fostering a culture of shared understanding and accountability.
- Knowledge sharing: ADRs help capture the collective knowledge and experience of the team, enabling future team members to learn from past decisions and avoid repeating mistakes.
