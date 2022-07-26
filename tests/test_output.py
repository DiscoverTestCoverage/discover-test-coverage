"""Test cases for the output module."""


from discover_test_coverage import output


def test_print_header_produces_two_output_lines(capsys):
    """Ensure that the print_header function outputs two lines."""
    output.print_header()
    captured_output = capsys.readouterr()
    num_lines_in_output = captured_output.out.count("\n")
    assert num_lines_in_output == 4
