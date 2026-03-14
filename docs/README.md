# Documentation

This folder contains detailed documentation for the AI Agent project.

## Quick Links

- **[Back to Main README](../README.md)**

## Documentation Files

### Getting Started
- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step guide to get up and running quickly
  - Installation steps
  - Configuration guide
  - First steps
  - Common issues

- **[QUICKSTART_API.md](QUICKSTART_API.md)** - FastAPI server quick start
  - Starting the server
  - Quick tests with cURL
  - Environment configuration
  - Troubleshooting

### API & Integration
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete FastAPI reference
  - All endpoints
  - Request/response formats
  - Authentication flow
  - Usage examples

- **[AUTHENTICATION.md](AUTHENTICATION.md)** - External authentication guide
  - Auth flow diagram
  - Per-request tokens
  - Implementation details
  - Security considerations

- **[POSTMAN_GUIDE.md](POSTMAN_GUIDE.md)** - Using the Postman collection
  - Import instructions
  - Collection structure
  - Example requests
  - Tips & tricks

### Architecture & Design
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and design principles
  - Core components
  - Design patterns
  - Data flow
  - Extensibility model

### Project Organization
- **[STRUCTURE.md](STRUCTURE.md)** - Modular structure overview
  - Directory layout
  - File organization
  - Module breakdown
  - Size comparisons (before/after refactoring)

- **[PROJECT_ORGANIZATION.md](PROJECT_ORGANIZATION.md)** - Current project layout
  - Clean structure guide
  - Usage workflows
  - File purposes
  - Running examples

### Change History
- **[TOOLS_REFACTORING.md](TOOLS_REFACTORING.md)** - Tools system refactoring details
  - What changed
  - Migration guide
  - New patterns
  - Benefits

- **[RESTRUCTURE_COMPLETE.md](RESTRUCTURE_COMPLETE.md)** - Project restructuring summary
  - Examples organization
  - File moves
  - Updated commands

## Component Documentation

Additional documentation exists in component folders:

- **[../ai_agent/providers/README.md](../ai_agent/providers/README.md)** - Adding new model providers
- **[../tools/README.md](../tools/README.md)** - Tools system complete guide
- **[../examples/README.md](../examples/README.md)** - Examples documentation

## Documentation Map

```
For...                          See...
─────────────────────────────────────────────────────────────
Getting started quickly         QUICKSTART.md
Using FastAPI server           QUICKSTART_API.md, API_DOCUMENTATION.md
Testing with Postman           POSTMAN_GUIDE.md, ../NudgeAI.postman_collection.json
Understanding auth flow         AUTHENTICATION.md
Understanding architecture      ARCHITECTURE.md
Project structure overview      STRUCTURE.md or PROJECT_ORGANIZATION.md
Adding tools                    ../tools/README.md
Adding model providers          ../ai_agent/providers/README.md
Example implementations         ../examples/README.md
Refactoring history            TOOLS_REFACTORING.md, RESTRUCTURE_COMPLETE.md
```

## Quick Start Path

1. **[QUICKSTART.md](QUICKSTART.md)** - Setup and configuration
2. **[../examples/README.md](../examples/README.md)** - Run examples
3. **[../tools/README.md](../tools/README.md)** - Create your tools
4. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Understand the design
5. **[../ai_agent/providers/README.md](../ai_agent/providers/README.md)** - Add new models (optional)

## Contributing

When adding new documentation:
- Place general project docs in this folder
- Place component-specific docs in their respective folders
- Update this README with links
- Keep filenames descriptive and consistent

## Overview

The project is organized as:
- **Root README.md** - Main entry point, overview, quick reference
- **docs/** (this folder) - Detailed documentation
- **Component READMEs** - Specific to each module (ai_agent, tools, examples)
