# Work Hours Parser

A Python tool that parses work hours from a raw text file and automatically writes the extracted data into a preformatted Excel spreadsheet.

The project was created to automate a repetitive process of transferring work-hour information from text into Excel while keeping the data structured and consistent.

## Features

-   Parse work shift information from a text file
-   Extract:

    -   date
    -   city/location
    -   start time
    -   end time
    -   total hours
    -   prevailing hours

-   Handle multi-line records
-   Normalize whitespace in input data
-   Use regular expressions for data extraction
-   Store parsed data using a Python `dataclass`
-   Write parsed data into a preformatted Excel template
-   Handle invalid input records without stopping the entire process
-   Log parsing and file-related errors
-   Automated tests with `pytest`

## Example

### Input

The parser accepts records similar to:

```text
1/03 Kirkland 8.00 - 3.00 7h

3/03 Seattle, Bellevue 6.00 - 5.30 11.5h

10 Linwood 7.00 - 1.30 6.5h Prevailing hours: 8.00 - 11.30 3.5h
```

Multi-line records are also supported:

```text
20 Lynnwood
6.00 - 3.30 9.5h
Prevailing hours: 7.00 - 1.30 6.5h
```

### Parsed data

The information is converted into structured `WorkShift` objects:

```python
WorkShift(
    date="10",
    start="7:00",
    end="1:30",
    city="Linwood",
    hours=6.5,
    prevailing_hours=3.5,
)
```

### Excel output

The parsed data is written into a preformatted Excel file.

For example:

| Date | Start | End  | City              | Hours | Prevailing Hours |
| ---- | ----- | ---- | ----------------- | ----: | ---------------: |
| 1/03 | 8:00  | 3:00 | Kirkland          |   7.0 |                  |
| 3/03 | 6:00  | 5:30 | Seattle, Bellevue |  11.5 |              3.5 |

### Main modules

#### `parser.py`

Responsible for:

-   reading the input file
-   normalizing whitespace
-   parsing individual records
-   extracting prevailing hours
-   validating parsed records
-   logging invalid entries

#### `models.py`

Contains the `WorkShift` dataclass used to represent parsed work shifts.

```python
@dataclass
class WorkShift:
    date: str
    start: str
    end: str
    city: str
    hours: float
    prevailing_hours: float | None = None
```

#### `excel.py`

Responsible for:

-   opening the Excel template
-   writing parsed data into the spreadsheet
-   saving the resulting workbook
-   handling Excel-related errors

#### `main.py`

Acts as the entry point and connects the parsing and Excel components.

## Technologies

-   **Python 3.11+**
-   **Regular Expressions (`re`)** — parsing semi-structured text
-   **openpyxl** — reading and writing Excel files
-   **dataclasses** — representing structured work-shift data
-   **logging** — application logging and error reporting
-   **pytest** — automated testing

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/work-hours-parser.git
cd work-hours-parser
```

Create a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Make sure the input text file and Excel template are available in the project directory.

Run:

```bash
python main.py
```

The application will:

1. Read the raw text file
2. Parse the work-hour records
3. Convert the data into `WorkShift` objects
4. Write the parsed data into the Excel template
5. Save the resulting Excel file

## Testing

The project uses `pytest` for automated testing.

Run all tests:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

The test suite covers:

-   whitespace normalization
-   regular work-shift parsing
-   prevailing-hours parsing
-   multi-line entries
-   multiple records
-   invalid records
-   Excel data writing
-   Excel column placement

## Error Handling

Invalid records do not stop the entire parsing process.

For example:

```text
WARNING: Could not parse entry: invalid input
INFO: Parsed 10 shifts, skipped 1 invalid entries
```

Critical file-related errors are also handled and logged, including:

-   missing input files
-   missing Excel templates
-   permission errors
-   inability to save the Excel file

## Development Goals

This project was built as a Python automation project and focuses on several common software-development practices:

-   separating responsibilities between modules
-   reusable functions
-   type hints
-   structured data models
-   regular expressions
-   error handling
-   logging
-   automated testing
-   working with external files
-   Excel automation
