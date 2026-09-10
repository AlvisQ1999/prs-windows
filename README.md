# PRS on Windows

Windows-compatible reproduction of the  
**Human-centered In-building Embodied Delivery Benchmark (PRS)**.

This repository is based on the official PRS delivery benchmark and contains the modifications required to run the environment on Windows.

## Original Project

- Official repository: https://github.com/PRS-Organization/prs-delivery
- PRS Challenge: https://prsorg.github.io/challenge
- CVPR 2024 Embodied AI Workshop: https://embodied-ai.org/
- Unity environment: https://huggingface.co/datasets/xzq1999/prs-env

PRS provides an indoor embodied delivery environment containing multi-floor spaces, human NPCs, objects, robot navigation, visual perception, manipulation, and natural-language delivery tasks.

---
## Requirements

The project uses:

- Windows 11
- Python `3.9`
- The project virtual environment `.venv`
- Unity executable in `unity/`

The currently verified baseline versions include:

```text
openai==2.48.0
httpx==0.27.2
torch==2.0.1
torchvision==0.15.2
transformers==4.40.2
typing_extensions==4.16.0
```

`torch==2.0.1` and `torchvision==0.15.2` are the matching PyTorch versions used by
the baseline. The tested local environment uses CPU builds.

Create or activate the project environment, then install the pinned requirements:

```powershell
cd D:\BUAA\03Research\Robotic\PRS\prs-delivery-main
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\prs_requirements.txt
python -m pip check
```

Always use the `.venv` interpreter explicitly when there is any doubt:

```powershell
.\.venv\Scripts\python.exe -m pip check
```

The first import of `robot.object_detection` may download
`IDEA-Research/grounding-dino-tiny` from Hugging Face. The model is cached in
the standard Hugging Face cache under the current user's profile.

## Unity Setup

Download the PRS Unity executable from the official PRS distribution page and
extract it into the repository's `unity/` directory:

https://docs.google.com/forms/d/e/1FAIpQLScrk25iSnnmOH8cj4eqD8lcALcj1Cx1bSiiTsw9q9DzvWnCig/viewform?usp=sf_link

For this Windows checkout, keep the existing compatibility paths:

```text
Unity executable:
./unity/PRS-Env.exe

Unity data:
unity/PRS-Env_Data/StreamingAssets/...
```

`PrsEnv(start_up_mode=1, rendering=1)` starts the Windows Unity executable
automatically and opens the Unity window. `PrsEnv(start_up_mode=0)` expects
Unity to be started manually first.

The existing Windows compatibility fix in
`env/npc_control.py` must also be preserved: `random_walk()` passes world
coordinates in the order `pos[0], pos[1], pos[2]`.

## LLM Configuration

`robot/llm_process.py` uses the OpenAI Python SDK Responses API:

```python
client.responses.create(...)
```

The current local configuration is an OpenAI-compatible endpoint and model
defined in that file. Configure the provider's API key there only for local
testing. Never put a real API key in this README, a committed source file,
`.env` file, or any authentication file.

The current local endpoint and model are:

```text
base_url = https://api2.xcodecli.com/v1
model = gpt-5.5
```

The current SDK requirement is:

```text
openai==2.48.0
```

The old SDK requirement is retained as a comment in `prs_requirements.txt`:

```text
# openai==1.30.5
```

Do not downgrade to `openai==1.30.5` when using `client.responses.create(...)`;
that SDK does not provide the `responses` client.

## Test LLM Connectivity

Run the text-only test before starting Unity or a delivery task:

```powershell
.\.venv\Scripts\python.exe -u .\llm_test.py
```

A successful result looks like:

```text
LLM response: '...'
```

This test imports Grounding DINO because `robot.llm_process` initializes it,
but it does not start Unity and does not run a delivery task.

## Run The Interactive Demo

Start the official interactive demo with:

```powershell
.\.venv\Scripts\python.exe .\prs_demo.py
```

The Unity window can be controlled manually. The project demo uses the
keyboard controls provided by the PRS environment for camera, robot, and
simulation-speed control.

To close a programmatic run, call `prs.finish_env()`. If a process is
interrupted, verify that no old `PRS-Env.exe` or Python PRS server is still
using port `8000` before starting another run.

## Run One Delivery Task

Edit `TASK_ID` in `task_test.py` to select a task from:

```text
task/dataset/deliver_task_test_set.json
```

Then run:

```powershell
.\.venv\Scripts\python.exe -u .\task_test.py
```

The current runner:

1. Starts Unity automatically.
2. Imports one task.
3. Runs the baseline with trace output.
4. Prints LLM and multimodal responses.
5. Evaluates the task.
6. Closes Unity in the `finally` block.

The runner installs a 30-second repeating Python stack trace so that long
navigation or Unity-response waits can be located. It does not impose a
global task timeout. Stop a run with `Ctrl+C` if it makes no progress, then
check and clean any remaining Unity or port-8000 processes.

## Run Dataset Evaluation

The dataset file contains 918 delivery tasks. The official scaffold is:

```powershell
.\.venv\Scripts\python.exe -u .\task_evaluation.py
```

At the current checkout, the call to `delivery_execution(...)` inside
`task_evaluation.py` is commented out. Therefore this script currently loads
tasks and evaluates the environment scaffold without running the baseline.
Do not use it as the first LLM or baseline test.

For a baseline test, use `task_test.py` first. After the single-task path is
validated, enable the baseline call in `task_evaluation.py` only when a full
918-task run is intended. A full run starts one Unity environment and may take
a long time.

## Evaluation Notes

The PRS evaluator checks whether the correct target object is grasped, whether
the target person is found, and whether the robot is sufficiently close to the
person while carrying the correct object. `delivery_task_evaluate(...)` also
releases a carried object while collecting the final evaluation state.

The baseline may complete language parsing and multimodal scene checks while
still failing later navigation, object selection, grasping, or NPC approach.
Always inspect the printed task result instead of treating Unity process
termination alone as task success.

## References

- PRS project: https://github.com/PRS-Organization/prs-delivery
- Grounding DINO: https://github.com/IDEA-Research/GroundingDINO
- PRS Platform API: `document/api.md`
