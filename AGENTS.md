# Agent Guidelines

## Commands
- **Build**: `[UPDATE WHEN PROJECT IS INITIALIZED]`
- **Lint**: `[UPDATE WHEN PROJECT IS INITIALIZED]`
- **Test all**: `[UPDATE WHEN PROJECT IS INITIALIZED]`
- **Test single**: `[UPDATE WHEN PROJECT IS INITIALIZED]`
- **Type check**: `[UPDATE WHEN PROJECT IS INITIALIZED]`
- **Dev server**: `[UPDATE WHEN PROJECT IS INITIALIZED]`
- **Install deps**: `[UPDATE WHEN PROJECT IS INITIALIZED]`

## Code Style & Architecture
- **Imports**: Use absolute imports, group by external/internal, sort alphabetically
- **Formatting**: Follow project's formatter configuration (Prettier/Black/etc)
- **Types**: Use explicit types, avoid `any`, prefer interfaces for objects
- **Naming**: camelCase for variables/functions, PascalCase for classes/components
- **Functions**: Keep functions small and focused, use descriptive names
- **Error Handling**: Use proper error types, handle errors at appropriate levels
- **Comments**: Only add when necessary to explain why, not what
- **File Structure**: Follow existing directory patterns and naming conventions

## Security & Performance
- **Secrets**: Never commit API keys, tokens, or sensitive data
- **Dependencies**: Audit new dependencies, prefer established packages
- **Performance**: Consider memory usage, avoid N+1 queries, use lazy loading
- **Validation**: Sanitize all inputs, validate at boundaries
- **Error Boundaries**: Implement proper error handling and recovery

## Debugging & Troubleshooting
- **Logging**: Use structured logging with appropriate levels
- **Testing**: Write unit tests for logic, integration tests for workflows
- **Debugging**: Use debugger over console.log, add breakpoints strategically
- **Error Messages**: Make errors actionable with context and suggestions

## Workflow
- **Branch Strategy**: Use feature branches, keep main stable
- **Commits**: Write clear, atomic commits with descriptive messages
- **Code Review**: Self-review changes before requesting review
- **Documentation**: Update docs when adding features or changing APIs
- **Backwards Compatibility**: Consider breaking changes carefully

## Requirements
- Always run lint and type check after code changes
- Follow existing patterns and conventions in the codebase
- Use the same libraries and frameworks already in use
- Write tests for new functionality
- Never use placeholders or pseudo code
- Verify changes work end-to-end before completing tasks 
