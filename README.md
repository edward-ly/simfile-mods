<!--
SPDX-FileCopyrightText: 2021 Edward Ly <contact@edward.ly>

SPDX-License-Identifier: CC-BY-4.0
-->

Simple Python scripts for [StepMania](https://github.com/stepmania/stepmania) that can modify simfiles in bulk.

### Available Scripts

- `add_offset.py`
  - Changes the timing offset by the specified number of seconds.
  - Usage: `add_offset.py [-d|--dir <directory>] [-o|--offset <offset>]`
  - Default values:
    - `<directory>`: the current directory
    - `<offset>`: +0.009 seconds (default for Simply Love or other ITG-like setups)
- `classic_scale.py`
  - Converts DDR X-scale ratings to old DDR/ITG ratings using the table below.
  Also updates any `group.ini` files to use the same scale.
  - Usage: `classic_scale.py [-d|--dir <directory>]`
  - Default values:
    - `<directory>`: the current directory
- `x_scale.py`
  - Converts old DDR/ITG ratings to DDR X-scale ratings using the table below.
  Some randomness has been introduced for in-between values, so the output may not be as accurate (compared to `classic_scale.py`).
  Also updates any `group.ini` files to use the same scale.
  - Usage: `x_scale.py [-d|--dir <directory>]`
  - Default values:
    - `<directory>`: the current directory

| X-Scale | Classic Scale |
| :------ | :------------ |
| 1-2     | 1             |
| 3       | 2             |
| 4-5     | 3             |
| 6       | 4             |
| 7-8     | 5             |
| 9       | 6             |
| 10-11   | 7             |
| 12      | 8             |
| 13-14   | 9             |
| 15-16   | 10            |
| 17      | 11            |
| 18      | 12            |
| 19      | 13            |
| 20      | 14            |
