using System;

public static class Renderer
{
    public static void PrintMaze(Maze maze, bool solved)
    {
        int w = maze.Width, h = maze.Height;
        var grid = maze.Grid;

        for (int y = 0; y < h; y++)
        {
            // Print top walls
            for (int x = 0; x < w; x++)
                Console.Write(grid[x, y].Walls[0] ? "##" : "# ");
            Console.WriteLine("#");

            // Print side walls and contents
            for (int x = 0; x < w; x++)
            {
                var cell = grid[x, y];
                Console.Write(cell.Walls[3] ? "#" : " ");

                if (x == 0 && y == 0)
                    Console.Write("S");
                else if (x == w - 1 && y == h - 1)
                    Console.Write("E");
                else if (solved && cell.InPath)
                    Console.Write("?");
                else
                    Console.Write(" ");
            }
            Console.WriteLine("#");
        }

        // Bottom border
        for (int x = 0; x < w; x++)
            Console.Write("##");
        Console.WriteLine("#");
    }
}
