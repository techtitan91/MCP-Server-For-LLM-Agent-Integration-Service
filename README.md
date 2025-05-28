# MCP-Server-For-LLM-Agent-Integration-Service

A server designed to expose PagerDuty API functionalities to Large Language Models (LLMs). This server is intended for programmatic use, featuring structured inputs and outputs.

## Overview

The **MCP-Server-For-LLM-Agent-Integration-Service** furnishes a collection of tools for interacting with the PagerDuty API. These utilities are crafted for use by LLMs to execute various operations on PagerDuty resources, such as incidents, services, teams, and users.

## Installation

### From PyPI

```bash
pip install mcp-server-for-llm-agent-integration-service
```

### From Source Code

```sh
# Clone the repository
git clone https://github.com/techtitan91/MCP-Server-For-LLM-Agent-Integration-Service
cd MCP-Server-For-LLM-Agent-Integration-Service

# Install dependencies
brew install uv
uv sync
```

## System Requirements

- Python 3.13 or higher
- PagerDuty API key

## Configuration

The **MCP-Server-For-LLM-Agent-Integration-Service** necessitates a PagerDuty API key to be defined in the environment variables:

```bash
PAGERDUTY_API_KEY=your_api_key_here
```

## Usage Instructions

### As a Goose Extension

```json
{
  "type": "stdio",
  "enabled": true,
  "args": ["run", "python", "-m", "pagerduty_mcp_server"],
  "commandInput": "uv run python -m pagerduty_mcp_server",
  "timeout": 300,
  "id": "mcp-server-for-llm-agent-integration-service",
  "name": "MCP Server For LLM Agent Integration Service",
  "description": "Server for PagerDuty API integration with LLMs",
  "env_keys": ["PAGERDUTY_API_KEY"],
  "cmd": "uv"
}
```

### As a Standalone Server

```sh
uv run python -m pagerduty_mcp_server
```

## Response Structure

All API responses adhere to a uniform format:

```json
{
  "metadata": {
    "count": int,  // Number of items in the result
    "description": "<str>"  // A brief summary of the results
  },
  "resource_type": [ // Always pluralized for consistency, even if only one result is returned
    {

    },
  ],
  "error": {  // Present only if an error occurred
    "message": "<str>",  // Human-readable error explanation
    "code": "<str>"  // Machine-readable error identifier
  }
}
```

### Error Management

When an error takes place, the response will incorporate an error object with the subsequent structure:

```json
{
  "metadata": {
    "count": 0,
    "description": "An error occurred while processing the request"
  },
  "error": {
    "message": "Invalid user ID was provided",
    "code": "INVALID_USER_ID"
  }
}
```

Common error situations include:

- Invalid resource identifiers (e.g., user_id, team_id, service_id)
- Missing mandatory parameters
- Invalid values for parameters
- API request failures
- Errors during response processing

### Parameter Validation

- All ID parameters must be valid PagerDuty resource identifiers.
- Date parameters are required to be valid ISO8601 timestamps.
- List parameters (e.g., `statuses`, `team_ids`) must include valid values.
- Invalid values within list parameters will be disregarded.
- Required parameters cannot be `None` or empty strings.
- For `statuses` in `list_incidents`, only `triggered`, `acknowledged`, and `resolved` are acceptable values.
- For `urgency` in incidents, only `high` and `low` are acceptable values.
- The `limit` parameter can be utilized to restrict the quantity of results returned by list operations.

### Rate Limiting and Pagination

- The server respects PagerDuty's API rate limits.
- The server automatically manages pagination for you.
- The `limit` parameter can be employed to control the number of results returned by list operations.
- If no limit is specified, the server will return up to `{pagerduty_mcp_server.utils.RESPONSE_LIMIT}` results by default.

### Example Usage (Python)

```python
from pagerduty_mcp_server import incidents
from pagerduty_mcp_server.utils import RESPONSE_LIMIT

# List all incidents (including resolved ones) for the current user's teams
incidents_list = incidents.list_incidents()

# List only active incidents
active_incidents = incidents.list_incidents(statuses=['triggered', 'acknowledged'])

# List incidents for specific services
service_incidents = incidents.list_incidents(service_ids=['SERVICE-1', 'SERVICE-2'])

# List incidents for specific teams
team_incidents = incidents.list_incidents(team_ids=['TEAM-1', 'TEAM-2'])

# List incidents within a specified date range
date_range_incidents = incidents.list_incidents(
    since='2024-03-01T00:00:00Z',
    until='2024-03-14T23:59:59Z'
)

# List incidents with a custom limit on the number of results
limited_incidents = incidents.list_incidents(limit=10)

# List incidents with the default response limit
default_limit_incidents = incidents.list_incidents(limit=RESPONSE_LIMIT)
```

## User Contextual Filtering

Many functions accept a `current_user_context` parameter (defaulting to `True`), which automatically filters results based on this context. When `current_user_context` is `True`, certain filter parameters cannot be used as they would conflict with this automatic filtering:

- For all resource categories:
  - `user_ids` cannot be used when `current_user_context=True`.
- For incidents:
  - `team_ids` and `service_ids` cannot be used when `current_user_context=True`.
- For services:
  - `team_ids` cannot be used when `current_user_context=True`.
- For escalation policies:
  - `team_ids` cannot be used when `current_user_context=True`.
- For on-calls:
  - `user_ids` cannot be used when `current_user_context=True`.
  - `schedule_ids` can still be employed to filter by specific schedules.
  - The query will display on-calls for all escalation policies associated with the current user's teams.
  - This is beneficial for answering questions like "who is presently on-call for my team?"
  - The current user's ID is not applied as a filter, so you'll observe all team members who are on-call.

## Development

### Executing Tests

Note that most tests necessitate a live connection to the PagerDuty API, so you will need to set the `PAGERDUTY_API_KEY` in your environment before running the complete test suite.

```bash
uv run pytest
```

To run only unit tests (i.e., tests that do not require `PAGERDUTY_API_KEY` to be set):

```bash
uv run pytest -m unit
```

To run only integration tests:

```bash
uv run pytest -m integration
```

To run only parser tests:

```bash
uv run pytest -m parsers
```

To run only tests pertaining to a specific submodule:

```bash
uv run pytest -m <client|escalation_policies|...>
```

### Debugging the Server with MCP Inspector

```bash
npx @modelcontextprotocol/inspector uv run python -m pagerduty_mcp_server
```

## Contributions

### Release Process

This project adheres to [Conventional Commits](https://www.conventionalcommits.org/) for automated releases. Commit messages dictate version increments:

- `feat:` → minor version (e.g., 1.0.0 → 1.1.0)
- `fix:` → patch version (e.g., 1.0.0 → 1.0.1)
- `BREAKING CHANGE:` → major version (e.g., 1.0.0 → 2.0.0)

The `CHANGELOG.md`, GitHub releases, and PyPI packages are updated automatically.

### Documentation Links

[Tool Documentation](https://www.google.com/search?q=./docs/tools.md) - Detailed information regarding available tools, including parameters, return types, and example queries.

### Coding Conventions

- All API responses follow the standardized format including metadata, a resource list, and an optional error object.
- Resource names in responses are consistently pluralized for uniformity.
- All functions that return a single item still yield a list containing one element.
- Error responses include both a human-readable message and a machine-readable code.
- All timestamps are formatted in ISO8601.
- Tests are marked with pytest markers to indicate their type (unit/integration), the resource they pertain to (incidents, teams, etc.), and whether they test parsing functionality (using the "parsers" marker).
