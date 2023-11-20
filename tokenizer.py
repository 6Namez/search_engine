import re


def tokenize(query_str):
    """
    Tokenizes the input string by splitting on whitespace and adding spaces around certain symbols.

    Args:
        query_str (str): The input string to tokenize.

    Returns:
        list: A list of tokens.
    """
    # Define symbols to add spaces around
    symbols = list('.,%$')
    # Add spaces around symbols
    for s in symbols:
        query_str = query_str.replace(s, f' {s} ')
    # Convert to lowercase and split on whitespace
    return query_str.lower().split()


def extract_unquoted_and_quoted(matches):
    """
    Separates quoted and unquoted parts from a list of matches.

    Args:
        matches (list): A list of string matches.

    Returns:
        tuple: A tuple containing two strings - quoted and unquoted parts.
    """
    unquoted_str = []
    quoted_str = []

    # Extract unquoted strings
    for match in matches:
        if not (match.startswith('"') and match.endswith('"')) and not (match.startswith("'") and match.endswith("'")):
            # Unquoted strings
            unquoted_str.append(match)
        elif match.startswith("'") and match.endswith("'"):
            # Single-quoted strings
            quoted_str.append(match.strip("'"))
        elif match.startswith('"') and match.endswith('"'):
            # Double-quoted strings
            quoted_str.append(match.strip('"'))

    # Join the unquoted and quoted strings
    unquoted_str = ' '.join(unquoted_str)
    quoted_str = ' '.join(quoted_str)

    # Return strings
    return unquoted_str, quoted_str


def quotation_parser(query_str):
    """
    Parses a query string, extracting quoted and unquoted parts, and tokenizing the resulting strings.

    Args:
        query_str (str): The input query string.

    Returns:
        tuple: A tuple containing two lists of tokens - quoted and unquoted tokens.
    """
    # Define a regular expression pattern to match quoted and unquoted parts
    pattern = re.compile(r'(\'[^\']*\'|"[^"]*"|\S+)')

    # Use findall to get all matches
    matches = pattern.findall(query_str)

    # Separate quoted and unquoted parts
    unquoted_str, quoted_str = extract_unquoted_and_quoted(matches)

    # Tokenize the resulting strings
    unquoted_tokens = tokenize(unquoted_str)
    quoted_tokens = tokenize(quoted_str)

    # returns are lists of tokens for quoted and unquoted
    return unquoted_tokens, quoted_tokens
