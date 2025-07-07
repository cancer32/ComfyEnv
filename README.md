# ComfyEnv: An Environment Manager for ComfyUI

ComfyUI is incredibly flexible, but installing different custom nodes or dependencies often leads to conflicts that can break existing setups. **ComfyEnv** helps you manage isolated environments, so each project or node set can live in its own stable sandbox.

> **Supported Platforms:**
>
> ✅ Windows
> ✅ Linux
> ❌ macOS is currently **not supported**

---

## Features

- Isolated **Conda environments** per ComfyUI setup
- Install and run ComfyUI without dependency conflicts
- Torch installation support (`--with-torch`)
- Clean separation of node configurations
- CLI tool for managing environments
- Built-in stop/start functionality for running ComfyUI instances

---

## Requirements

Before using ComfyEnv, make sure the following are installed:

- [Miniconda3](https://docs.conda.io/en/latest/miniconda.html)
- [Git](https://git-scm.com/)

---

## Installation

```bash
git clone https://github.com/yourusername/comfyenv.git
cd comfyenv
pip install -r requirements.txt
```

---

## Environment Variables
> ⚠️ Set the `CONDA_ROOT` environment variable manually.

| Variable     | Description                              | Example                     |
| ------------ | ---------------------------------------- | --------------------------- |
| `CONDA_ROOT` | Root path of your Miniconda installation | `C:\ProgramData\miniconda3` |

---

## Usage

### Create a new environment

```bash
comfyenv create my-env --python=3.10 --with-torch
```

### List all environments

```bash
comfyenv list
```

### Run ComfyUI inside an environment

```bash
comfyenv run -n my-env -- [comfyui args]
```

### Stop ComfyUI running in an environment

```bash
comfyenv stop -n my-env
```

---

## TODO

- [x] Project structure
- [x] Create environment
- [x] List environments
- [x] Run ComfyUI from environment
- [x] Stop ComfyUI
- [ ] **Remove environment**
  - `comfyenv remove -n <env-name>`
- [ ] **Update environment**
  - `comfyenv update -n <env-name>`
- [ ] **Activate env for manual dependency installation**
  - `comfyenv activate -n <env-name> --conda-only`
- [ ] **GUI or tray icon for quick switching** (optional)
