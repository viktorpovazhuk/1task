"""
Examine skyscrapers game board.

GitHub: https://github.com/viktorpovazhuk/skyscrapers
"""


def read_input(path: str) -> list:
    """
    Read game board file from path.
    Return list of str.
    """
    with open(path) as efile:
        lines = efile.readlines()
    lines = [line.strip("\n") for line in lines]
    # print(len(lines))
    return lines


def left_to_right_check(input_line: str, pivot: int) -> bool:
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    >>> left_to_right_check("41*453*", 3)
    True
    """
    heights = input_line[1:-1]
    cur = 0
    vis = 0
    for height in heights:
        if height == "*":
            continue
        if int(height) > cur:
            vis += 1
            cur = int(height)
    if vis == pivot:
        return True
    return False


def check_not_finished_board(board: list) -> bool:
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', \
        '*?????5', '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', \
        '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', \
        '*5?3215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board:
        if "?" in row:
            return False
    return True


def check_uniqueness_in_rows(board: list) -> bool:
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', \
        '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', \
        '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', \
        '*553215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board[1:-1]:
        uniq_chars = []
        for char in row[1:-1]:
            if char == "*":
                continue
            elif char not in uniq_chars:
                uniq_chars.append(char)
            else:
                return False
    return True


def check_horizontal_visibility(board: list) -> bool:
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', \
        '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', \
        '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', \
        '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board:
        left_vis = True if row[0] == "*" else left_to_right_check(
            row, int(row[0]))
        # try:
        #     left_vis = True if row[0] == "*" else left_to_right_check(row, int(row[0]))
        # except:
        #     print(row)
        right_vis = (
            True if row[-1] == "*" else left_to_right_check(
                row[::-1], int(row[-1]))
        )
        if not left_vis or not right_vis:
            return False
    return True


def check_columns(board: list) -> bool:
    """
    Check column-wise compliance of the board for
    uniqueness (buildings of unique height) and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    columns = []
    for i in range(1, len(board[0]) - 1):
        col = [board[row][i] for row in range(0, len(board))]
        columns.append("".join(col))
    # print(columns)
    vis = check_horizontal_visibility(columns)
    uniq = check_uniqueness_in_rows(columns)
    if vis and uniq:
        return True
    return False


def check_skyscrapers(input_path: str) -> bool:
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.
    """
    board = read_input(input_path)
    if (check_not_finished_board(board) and check_uniqueness_in_rows(board)
            and check_horizontal_visibility(board) and check_columns(board)):
        return True
    return False


if __name__ == "__main__":
    # print(check_skyscrapers("check.txt"))
    import doctest

    doctest.testmod()

    # >>> check_skyscrapers("check.txt")
    # True
