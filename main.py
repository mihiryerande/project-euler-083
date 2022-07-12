# Problem 83:
#     Path Sum: Four Ways
#
# Description:
#     NOTE: This problem is a significantly more challenging version of Problem 81.
#
#     In the 5 by 5 matrix below,
#       the minimal path sum from the top left to the bottom right,
#       by moving left, right, up, and down,
#       is indicated in bold red and is equal to 2297.
#
#         | [131]  673  [234] [103] [ 18] |
#         | [201] [ 96] [342]  965  [150] |
#         |  630   803   746  [422] [111] |
#         |  537   699   497  [121]  956  |
#         |  805   732   524  [ 37] [331] |
#
#     Find the minimal path sum from the top left to the bottom right by moving left, right, up, and down
#       in matrix.txt (right click and "Save Link/Target As..."), a 31K text file containing an 80 by 80 matrix.

from numpy import inf
from typing import List, Tuple


def main(filename: str) -> Tuple[int, List[str]]:
    """
    Returns the minimal path sum in the given `filename`
      starting from the top-left cell and
      finishing in the bottom-right cell,
      taking steps left, right, up, and down.

    Args:
        filename (str): File name containing integer matrix

    Returns:
        (Tuple[int, List[str]]):
           Minimal path sum walking from top-left to bottom-right in matrix, stepping in any direction

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(filename) == str

    # Idea:
    #     Maintain a grid where each cell stores:
    #       * The least sum of any path starting from the top-left and ending at that cell
    #       * The direction of the previous cell in that path
    #
    #     Continually update this grid by maintaining a queue of cells to be updated.
    #     Any time the value in a visited cell is changed,
    #       add its neighbors to the queue to be updated as well.
    #     Do this until the queue is empty, meaning no further updates are possible.
    #
    #     Then simply check the final cell to get the sum of the minimal path ending there,
    #       and backtrack through the path to determine the step directions in reverse.

    # Read integer matrix
    with open(filename, 'r') as f:
        m = list(map(lambda line: list(map(int, line.split(','))), f.readlines()))

    # Assume given matrix is square
    n = len(m)

    # Grid to keep track of minimal sub-path sum ending at current point
    grid_sum: List[List[int]] = [[inf for _ in range(n)] for _ in range(n)]
    grid_sum[0][0] = m[0][0]

    # Grid to keep track of direction of previous cell in minimal paths
    grid_dir = [['' for _ in range(n)] for _ in range(n)]

    # Queue of cells to be updated, starting with neighbors of top-left cell
    q = [(0, 1), (1, 0)]

    # Update cells until no more updates left to make
    while len(q) > 0:
        py, px = q.pop(0)
        if 0 <= py < n and 0 <= px < n:
            all_choices = [
                (py, px-1, 'L'),  # Left
                (py, px+1, 'R'),  # Right
                (py-1, px, 'U'),  # Up
                (py+1, px, 'D')]  # Down

            # Filter to useful ones
            choices = [c for c in all_choices if 0 <= c[0] < n and 0 <= c[1] < n and grid_sum[c[0]][c[1]] < inf]

            # Pick best of those
            min_choice = min(choices, key=lambda c: grid_sum[c[0]][c[1]])
            qy, qx = min_choice[:2]
            curr_elt = m[py][px]
            new_sum = grid_sum[qy][qx] + curr_elt
            if grid_sum[py][px] is None or new_sum < grid_sum[py][px]:
                # Update grid with new minimal sum
                grid_sum[py][px] = new_sum
                grid_dir[py][px] = min_choice[2]

                # Add neighbors to be checked again
                q += list(map(lambda c: c[:2], all_choices))
            else:
                # Cell already has best known sum as of now
                pass
        else:
            # Point is out-of-bounds, so ignore
            pass

    # Walk backwards through grid, from bottom-left to top-right, enumerating minimal path
    py = px = n-1
    path_sum = grid_sum[py][px]
    fwd_path = []
    while py > 0 and px > 0:
        if grid_dir[py][px] == 'L':
            fwd_dir = 'R'
            px -= 1
        elif grid_dir[py][px] == 'R':
            fwd_dir = 'L'
            px += 1
        elif grid_dir[py][px] == 'U':
            fwd_dir = 'D'
            py -= 1
        else:
            # grid_dir[py][px] == 'D':
            fwd_dir = 'U'
            py += 1
        fwd_path.append(fwd_dir)
    fwd_path.reverse()

    return path_sum, fwd_path


if __name__ == '__main__':
    matrix_filename = 'matrix.txt'
    minimal_path_sum, minimal_path = main(matrix_filename)
    print('Minimal path sum in "{}":'.format(matrix_filename))
    print('  {}'.format(minimal_path_sum))
    print('Path producing that sum:')
    print('  Start at top-left -> {}'.format(' -> '.join(minimal_path)))
