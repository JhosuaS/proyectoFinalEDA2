def bad_character(pattern):
    """
    Construye la tabla de último índice de aparición
    de cada carácter del patrón.
    """
    table = {}

    for i, c in enumerate(pattern):
        table[c] = i

    return table


def bm(text, pattern):
    n = len(text)
    m = len(pattern)

    if n == 0 or m == 0:
        return 0

    bad = bad_character(pattern)
    matches = []

    s = 0

    while s <= n - m:

        j = m - 1

        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:

            matches.append(s)

            if s + m < n:
                s += m - bad.get(text[s + m], -1)
            else:
                s += 1

        else:

            shift = max(1, j - bad.get(text[s + j], -1))
            s += shift

    return None if not matches else matches
