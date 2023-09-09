import re


def remove_redundant_newlines(text):
    """Removes redundant newlines from the text."""
    return re.sub(r'\n+', '\n', text)


def convert_tabs_to_spaces(text, tab_width=4):
    """Converts all tabs to spaces in the text."""
    return text.replace('\t', ' ' * tab_width)


def remove_redundant_spaces(text):
    """Removes all redundant spaces from the text."""
    return re.sub(r' +', ' ', text)
