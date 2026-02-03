using System.Collections.Generic;

public class Solver
{
    private Maze maze;
    private Cell endCell;
    private bool solved = false;

    public Solver(Maze maze)
    {
        this.maze = maze;
        endCell = maze.GetEndCell();
    }

    public bool Solve()
    {
        return DFS(maze.GetStartCell(), new HashSet<Cell>());
    }

    private bool DFS(Cell cell, HashSet<Cell> visited)
    {
        visited.Add(cell);

        if (cell == endCell)
        {
            cell.InPath = true;
            return true;
        }

        int x = cell.X, y = cell.Y;
        var directions = new (int dx, int dy, int wall)[]
        {
            (0, -1, 0), // Top
            (1, 0, 1),  // Right
            (0, 1, 2),  // Bottom
            (-1, 0, 3), // Left
        };

        foreach (var (dx, dy, wall) in directions)
        {
            int nx = x + dx, ny = y + dy;
            if (nx < 0 || ny < 0 || nx >= maze.Width || ny >= maze.Height)
                continue;

            if (!cell.Walls[wall])
            {
                Cell neighbor = maze.Grid[nx, ny];
                if (!visited.Contains(neighbor))
                {
                    if (DFS(neighbor, visited))
                    {
                        cell.InPath = true;
                        return true;
                    }
                }
            }
        }

        return false;
    }
}
