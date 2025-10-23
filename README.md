# Eight Puzzle (PA1 Search) — Code and Usage

This folder contains `eightpuzzle.py`, which provides a command-line interface to run several search algorithms on the 8-puzzle domain. Use the instructions below to run Greedy Best-First Search (GBS) with both heuristics and produce the output files required by the assignment.

## Prerequisites
- Python 3.8+ installed and available as `python` in PowerShell.
- No extra Python packages are required (uses stdlib).

## Files
- `eightpuzzle.py` — main script (accepts `--search`, `--initial`, `--goal`, `--heuristic`).
- `run_both.ps1` — small PowerShell helper that runs GBS twice (misplaced and manhattan) and lists results.

## Typical usage

Open a PowerShell prompt in this folder (the `PA1_Search/Code` directory) then run a single GBS run like:

```powershell
python .\eightpuzzle.py --search GBS --initial "[[-,2,3],[1,4,5],[8,7,6]]" --goal "[[1,2,3],[8,-,4],[7,6,5]]" --heuristic misplaced
```

This will create an output file named `output_GBS_misplaced.txt` in the same folder.

To run the same problem with the Manhattan heuristic:

```powershell
python .\eightpuzzle.py --search GBS --initial "[[-,2,3],[1,4,5],[8,7,6]]" --goal "[[1,2,3],[8,-,4],[7,6,5]]" --heuristic manhattan
```

## Run both heuristics automatically (PowerShell)
If you prefer to run both heuristics automatically, use the helper script:

```powershell
./run_both.ps1
```

The helper runs GBS twice (misplaced then manhattan) with the example initial/goal above and prints the resulting filenames. You can edit `run_both.ps1` to change the `--initial` and `--goal` values.

## Notes
- The script writes output files in the current working directory with names like `output_GBS_misplaced.txt` and `output_GBS_manhattan.txt`.
- If you encounter filename or path errors on Windows, ensure the filenames do not contain characters forbidden by Windows (e.g., `* ? < > |`).

If you'd like, I can also add a small README at the repo root linking to this file or modify `eightpuzzle.py` to add a `--both` flag that automatically runs both heuristics. Let me know which you prefer.
