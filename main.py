import logging

from text_parser import read_input_file, parse_timesheet
from excel import write_to_excel


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


def main() -> None:
    input_path = "raw data.txt"
    template_path = "work hours.xlsx"
    output_path = "work hours.xlsx"

    text = read_input_file(input_path)

    shifts = parse_timesheet(text)

    write_to_excel(
        shifts=shifts,
        template_path=template_path,
        output_path=output_path,
    )


if __name__ == "__main__":
    main()
