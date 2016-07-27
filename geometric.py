def geometric_chain(s1, s2, start=""):
    """ s1 and s2 are lists of strings, aka:
        ["AB", "XLMQ"]; ["AXB", "LZ"]
    """
    ALPHA_LEN = 26
    ls = s1 + s2
    if start:
        ls = [l for l s1 + s2 if start in l]
    if not ls:
        return None * 3

    start_s = max(ls, key=len)
    grid = [[DIT for i in range(ALPHA_LEN)] for j in range(ALPHA_LEN)]
    for idx, letter in enumerate(start_s):
        if start_s in s2:
            grid[idx % ALPHA_LEN][0] = letter
        else:
            grid[0][idx % ALPHA_LEN] = letter

    change = 1
    already_seen = set()
    while change:
        change = 0
        error = 0
        for trow, tcol in itertools.product(range(ALPHA_LEN), range(ALPHA_LEN)):
            if (trow, tcol) in already_seen:
                continue
            tletter = grid[trow][tcol]
            if tletter == DIT:
                continue
            already_seen.add((trow, tcol))
            down = [l for l in s2 if tletter in l]
            if down:
                nchange, nerr = update_grid(tletter, trow, tcol, down[0],
                                            DOWN, grid)
                change += nchange
                error += nerr

            across = [l for l in s1 if letter in l]
            if across:
                nchange, nerr = update_grid(tletter, trow, tcol, across[0],
                                            ACROSS, grid)
                change += nchange
                error += nerr

            if error:
                return None * 3
        s1 = recalculate_strs(s1, grid, ACROSS)
        s2 = recalculate_strs(s2, grid, DOWN)
        return grid, s1, s2


def update_grid(letter, row, col, s, direction, grid):
    idx = s.index(letter)
    new_row, new_col = row, col
    change = 0
    err = 0
    for i, l in enumerate(s):
        if direction == DOWN:
            new_row = (i - idx + row) % ALPHA_LEN
        else:
            new_col = (i - idx + col) % ALPHA_LEN
        if grid[new_row][new_col] == DIT:
            grid[new_row][new_col] = letter
            change += 1
        elif grid[new_row][new_col] != letter:
            err += 1
    return change, err

def recalculate_strs(strings, grid, direction):
    pairs = set()
    loops = []
    if direction == DOWN:
        ## literally no idea what this purports to do
        for col in range(ALPHA_LEN):
            loops.extend([l for l in ("".join(grid[i][col]
                for i in range(ALPHA_LEN)) + grid[0][col]).split(DIT)
                if len(l) >= 2])
    else:
        for row in range(ALPHA_LEN):
            loops.extend([l for l in ("".join(grid[row]) +
                grid[row][0]).split(DIT) if len(l) >= 2])
    for loop in loops:
        for i in range(len(loop) - 1):
            pairs.add(loops[i:i+2])
    for s in strings:
        if not any(s[0] in string for string in pairs):
            pairs.add(s)
    return list(pairs)

def print_geometric_grid(grid):
    print("\n".join(" ".join(row) for row in grid))

