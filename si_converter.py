def si_converter(size_kb):
    """
    Pass size in kB and convert to SI string with 2 significant figures.

    k: 10^3
    M: 10^6
    G: 10^9
    T: 10^12
    P: 10^15
    """
    assert len(size_kb)
    prefixes = ["kB", "MB", "GB", "TB", "PB"]
    prefix_idx = 0
    size_kb = int(size_kb)
    while(size_kb > 1000) and prefix_idx < len(prefixes) - 1:
        size_kb = round(size_kb/1000, 1)
        prefix_idx += 1

    sig_figs = 0
    for digit in str(size_kb):
        if digit != '0' and digit != '.':
            sig_figs += 1

    if sig_figs > 2:
        size_kb = int(round(size_kb))
    elif str(size_kb)[-1] == '0':
        size_kb = int(size_kb)

    return str(size_kb) + prefixes[prefix_idx]

def main():
    assert si_converter("4")           == "4kB"
    assert si_converter("52")          == "52kB"
    assert si_converter("520")         == "520kB"
    assert si_converter("9999")        == "10MB", si_converter("9999")
    assert si_converter("99990")       == "100MB", si_converter("99990")
    assert si_converter("999901")      == "1000MB", si_converter("999901")
    assert si_converter("42000000000") == "42TB", si_converter("42000000000")
    assert si_converter("4200000000000") == "4.2PB", si_converter("4200000000000")
    assert si_converter("42000000000000000") == "42000PB", si_converter("42000000000000000")

if __name__ == '__main__':
    main()
