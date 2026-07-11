def failure(pattern):
    m = len(pattern)

    if m == 0: return 0

    prefix_f = [0] * m
    k = 0 
    j = 1

    while j < m:
        if pattern[j] == pattern[k]:
            prefix_f[j] = k + 1
            j += 1
            k += 1
        
        elif k > 0:
            k = prefix_f[k - 1]
        
        else:
            j += 1

    return prefix_f

def kmp(text, pattern):
    n, m = len(text), len(pattern)

    if m == 0 or n == 0: return 0

    f = failure(pattern)
    j = k = 0
    matches = []

    while j < n:
        if text[j] == pattern[k]:
            j += 1
            k += 1

            if k == m:
                matches.append(j - k)
                k = f[k - 1]

        elif k > 0:
            k = f[k - 1]
        
        else:
            j += 1

    return None if not matches else matches



