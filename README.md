# AIAgent

**AIAgent** is a Python framework designed to be a **universal AI assistant wrapper** for multiple generative APIs.
It allows AI models to call tools or APIs recursively, handle their responses, and integrate them into multi-turn conversations.

The project is organized into API-specific modules, each in its own folder (e.g., `gemini/`). New APIs can be added easily.

---

## Project Structure

```
AssistantAI/
│
├─ gemini/                 # Wrapper and tools for Google Gemini
│   ├─ assistant_ai.py     # Main Gemini integration
│   └─ tools/              # Example tools for Gemini
│
├─ openai/                 # Planned: wrapper for OpenAI APIs
│
├─ whisper/                # Planned: speech-to-text integration
│
└─ examples/               # Usage examples
```

---

## Features

* Unified interface for multiple generative AI APIs
* Recursive handling of function/tool calls
* Automatic parsing of model responses (text or function calls)
* Context management for multi-turn conversations
* Configurable maximum recursion depth
* Support for `system`, `user`, and `function` roles
* Modular architecture: add new APIs by creating a folder/module

---

## How It Works

1. **Initialize** the assistant with configuration: API keys, model name, system instructions, and tools.
2. **Interact** via `interaction(context)` with a list of messages.
3. **Handle responses**:

   * Function calls → execute tool/API → feed response back
   * Text → append to conversation
4. **Recursion** is handled automatically up to a configurable maximum depth.

---

## Status

🚧 **Work in progress**

* Gemini integration works (recursive tool handling included)
* Other APIs planned: OpenAI, Whisper, etc.
* All contributions to add API wrappers, tools, or improvements are welcome

---

## Contributing

All contributions are highly welcome!

* Add new API wrappers (OpenAI, Whisper, etc.)
* Implement additional tools/functions for existing APIs
* Improve recursive interaction handling
* Enhance logging, error handling, and examples

> This project is a collaborative experiment — help is greatly appreciated!

---

## Dependencies

```bash
pip install google-generativeai torch
```

Python 3.9+ recommended.
