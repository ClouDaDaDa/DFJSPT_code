﻿# Hierarchical Multi-Agent DRL for Dynamic Flexible Job-Shop Scheduling with Transportation (DFJSP-T)

## Overview

This project provides a solution for the **Dynamic Flexible Job-Shop Scheduling Problem with Transportation** (DFJSP-T) using a **Hierarchical Multi-Agent Deep Reinforcement Learning (DRL)** framework combined with **Imitation Learning (IL)**. The approach aims to optimize job-shop scheduling by integrating the transportation of robots (transbots) for job completion. It decomposes the problem into three decision levels:

1. **High-level Agent:** Prioritizes jobs to be processed.
2. **Mid-level Agent:** Selects machines for each assigned job.
3. **Low-level Agent:** Manages the transportation (transbot) between machines and jobs.

The project includes several components such as environment setups, agent models, dispatching rules, data generation, and training scripts, which together help to solve the scheduling problem efficiently.

## Project Structure

### `DFJSPT` (Dynamic Flexible Job-Shop Scheduling with Transportation)
- `dfjspt_agent_model.py`: Defines the agent model for DFJSP-T.
- `dfjspt_env.py`: Environment setup for DFJSP-T.
- `dfjspt_params.py`: Parameters and configurations for DFJSP-T.
- `dfjspt_rule/`: A collection of dispatching rules for job selection, machine selection, and transbot selection.
- `dfjspt_train.py`: Training script specific to DFJSP-T.
- `dfjspt_test.py`: Test script for DFJSP-T experiments.
- `dfjspt_data/`: Data-related utilities and generators for DFJSP-T experiments.

## Installation

Clone this repository to your local machine:
   ```bash
   git clone https://github.com/ClouDaDaDa/dfjspt_code.git
   cd dfjsp_code
   ```

## Usage

### Training a Model
To train the model for DFJSP-T, use the following script:
```bash
python DFJSPT/dfjspt_train.py
```

This will initialize the environment, agent, and training loop, utilizing DRL and imitation learning strategies.

### Testing a Model
To test a trained model:
```bash
python DFJSPT/dfjspt_test.py
```

### Running Experiments
For running experiments with different dispatching rules and scheduling heuristics, you can modify and execute the scripts in the `dispatching_rules/` directory.

## Configuration

All training parameters, such as learning rates, batch sizes, and environment configurations, can be modified in the `params.py` file located in the root directory.

