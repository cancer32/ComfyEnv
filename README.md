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
conda activate
git clone https://github.com/cancer32/ComfyEnv.git
cd ComfyEnv
pip install -r requirements.txt
```

---

## Environment Variables
> ⚠️ Set the `CONDA_ROOT` environment variable manually.

| Variable     | Description                              | Example                     |
| ------------ | ---------------------------------------- | --------------------------- |
| `CONDA_ROOT` | Root path of your Miniconda installation | `C:\ProgramData\miniconda3` |

---

### Directory Structure

```
ComfyEnv/
├── bin/
│   └── comfyenv         # The main CLI script or executable
├── envs/                # Contains all isolated environments
│   └── <env_name>/      # A specific ComfyUI environment
├── models/              # Shared models directory accessible from all environments
│   └── checkpoints/
│   └── vae/
│   └── .../
```
---

## Usage

### Create a new environment

```bash
bin/comfyenv create my-env --python=3.10 --comfyui-version=v0.3.43
```
> Note: Edit **torch_requirements.txt** file if you want to install specific pytorch version in the environment 


### List all environments

```bash
bin/comfyenv list
```

### Run ComfyUI inside an environment

```bash
bin/comfyenv run -n my-env -- [comfyui args]
```

### Stop ComfyUI running in an environment

```bash
bin/comfyenv stop -n my-env
```

---

## TODO

- [x] Project structure
- [x] Create environment
- [x] List environments
- [x] Run ComfyUI from environment
- [x] Stop ComfyUI
- [X] Remove environment
- [X] Update environment
- [X] Activate env for manual dependency installation
- [ ] **GUI or tray icon for quick switching** (optional)
