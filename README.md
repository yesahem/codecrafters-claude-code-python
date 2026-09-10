# LLM Coding Agent with Tool Calling (Claude Code Clone)

[![progress-banner](https://backend.codecrafters.io/progress/claude-code/3910deae-0e74-4f1e-8e52-d3ba441714a4)](https://app.codecrafters.io/users/yesahem?r=2qF)

A CLI coding agent that sends prompts to **Claude Haiku** through **OpenRouter**'s OpenAI-compatible API, then uses **function calling** and a multi-turn **agent loop** to read files, write edits, and run shell commands until the task is done.

Built for the [CodeCrafters "Build Your Own Claude Code"](https://codecrafters.io/challenges/claude-code) challenge. All 6 stages are complete.

## What it does

- Routes a `-p` prompt to Claude via OpenRouter (`chat.completions`)
- Advertises three JSON Schema tools: **Read**, **Write**, and **Bash**
- Runs an agent loop: call the model → execute tool calls → append results → repeat until a final text answer
- Uses local filesystem I/O and `subprocess` so the model can inspect code, apply edits, and run commands

## How the agent loop works

1. Send the user prompt plus tool definitions to the model (`tool_choice=auto`).
2. If the model returns tool calls, execute each one and append a `role: tool` message.
3. Call the model again with the updated conversation history.
4. Stop when the model returns a normal assistant message (no tool calls) and print that answer.

```
User prompt
    ↓
Claude (OpenRouter / OpenAI-compatible API)
    ↓
tool calls? ──yes──► Read / Write / Bash ──► append tool results ──┐
    │ no                                                          │
    ↓                                                             │
print final answer ◄──────────────────────────────────────────────┘
```

## Tools

| Tool | Purpose | Arguments |
| --- | --- | --- |
| `Read` | Return the contents of a file | `file_path` |
| `Write` | Create or overwrite a file | `file_path`, `content` |
| `Bash` | Run a shell command and capture stdout | `command` |

## Technologies

Python · OpenAI Python SDK · OpenRouter · Claude Haiku · Function / Tool Calling · JSON Schema · Agent Loop · argparse · subprocess · uv

## Setup

1. Install [uv](https://docs.astral.sh/uv/).
2. Set your OpenRouter credentials:

```sh
export OPENROUTER_API_KEY="your-key"
# optional; defaults to https://openrouter.ai/api/v1
export OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"
```

3. Run a prompt:

```sh
./your_program.sh -p "Read README.md and summarize it"
```

The entry point is `app/main.py`.

## Challenge stages

1. Communicate with the LLM
2. Advertise the Read tool
3. Execute the Read tool
4. Implement the agent loop
5. Implement the Write tool
6. Implement the Bash tool
