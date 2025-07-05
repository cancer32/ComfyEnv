# ComfyEnv: An environment manager for ComfyUI 

ComfyUI is incredibly flexible, but installing different custom nodes or dependencies often leads to conflicts that can break existing setups. ComfyEnv helps you manage isolated environments, so each project or node set can live in its own stable sandbox.


## Requirements

- Miniconda3
- Git


## Environment Variables

| Variable     | Description                              | Example                     |
| ------------ | ---------------------------------------- | --------------------------- |
| `CONDA_ROOT` | Root path of your Miniconda installation | `C:\ProgramData\miniconda3` |


## TODO:

- [ ] Project structure
- [ ] Create environment
	- comfyenv create <env-name> --python=3.10 --no-torch
- [ ] Query/list environment
	- comfyenv --list
- [ ] Remove environment
	- comfyenv remove <env-name>
- [ ] Run ComfyUI from an environment
	- comfyenv run <env-name> -- [confyui args]
- [ ] Activate env for manual dependency installation
	- comfyenv activate <env-name> --conda-only
- [ ] GUI or tray icon for quick switching (optional)