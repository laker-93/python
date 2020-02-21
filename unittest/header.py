def is_valid_header(header):
    try:
        title = header.split()[0]
        border = header.split()[1]
    except IndexError:
        return False
    if isinstance(header, str) and len(title) + 2 == len(border):
        return True
