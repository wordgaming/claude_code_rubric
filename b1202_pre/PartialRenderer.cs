using System;

public static class PartialRenderer
{
    // 渲染带有战争迷雾的迷宫
    public static void PrintMaze(Maze maze, PartialObservabilitySolver solver, bool solved)
    {
        int w = maze.Width, h = maze.Height;
        var grid = maze.Grid;

        Console.WriteLine("\n=== 部分可观察性迷宫 (战争迷雾) ===");
        Console.WriteLine("图例: S=起点 E=终点 ?=路径 ░=未探索 #=墙壁\n");

        for (int y = 0; y < h; y++)
        {
            // 打印顶部墙壁
            for (int x = 0; x < w; x++)
            {
                var cell = grid[x, y];
                
                if (!cell.Explored)
                {
                    // 未探索区域显示为迷雾
                    Console.Write("░░");
                }
                else
                {
                    // 已探索区域显示墙壁信息
                    if (cell.WallsKnown[0])
                    {
                        Console.Write(cell.Walls[0] ? "##" : "# ");
                    }
                    else
                    {
                        Console.Write("░░");
                    }
                }
            }
            Console.WriteLine("#");

            // 打印侧墙和内容
            for (int x = 0; x < w; x++)
            {
                var cell = grid[x, y];
                
                if (!cell.Explored)
                {
                    // 未探索区域
                    Console.Write("░░");
                }
                else
                {
                    // 左墙
                    if (cell.WallsKnown[3])
                    {
                        Console.Write(cell.Walls[3] ? "#" : " ");
                    }
                    else
                    {
                        Console.Write("░");
                    }

                    // 单元格内容
                    if (x == 0 && y == 0)
                        Console.Write("S");
                    else if (x == w - 1 && y == h - 1)
                        Console.Write("E");
                    else if (solved && cell.InPath)
                        Console.Write("?");
                    else if (cell.Visited)
                        Console.Write("·"); // 已访问但不在路径上
                    else
                        Console.Write(" ");
                }
            }
            Console.WriteLine("#");
        }

        // 底部边界
        for (int x = 0; x < w; x++)
        {
            var cell = grid[x, h - 1];
            if (cell.Explored && cell.WallsKnown[2])
            {
                Console.Write("##");
            }
            else
            {
                Console.Write("░░");
            }
        }
        Console.WriteLine("#");
    }

    // 渲染完整迷宫（用于对比）
    public static void PrintFullMaze(Maze maze, bool solved)
    {
        int w = maze.Width, h = maze.Height;
        var grid = maze.Grid;

        Console.WriteLine("\n=== 完整迷宫 (无迷雾) ===");
        Console.WriteLine("图例: S=起点 E=终点 ?=路径 #=墙壁\n");

        for (int y = 0; y < h; y++)
        {
            // 打印顶部墙壁
            for (int x = 0; x < w; x++)
                Console.Write(grid[x, y].Walls[0] ? "##" : "# ");
            Console.WriteLine("#");

            // 打印侧墙和内容
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

        // 底部边界
        for (int x = 0; x < w; x++)
            Console.Write("##");
        Console.WriteLine("#");
    }

    // 显示探索统计
    public static void PrintStatistics(Maze maze)
    {
        int totalCells = maze.Width * maze.Height;
        int exploredCells = 0;
        int visitedCells = 0;
        int pathCells = 0;

        for (int x = 0; x < maze.Width; x++)
        {
            for (int y = 0; y < maze.Height; y++)
            {
                var cell = maze.Grid[x, y];
                if (cell.Explored) exploredCells++;
                if (cell.Visited) visitedCells++;
                if (cell.InPath) pathCells++;
            }
        }

        Console.WriteLine("\n=== 探索统计 ===");
        Console.WriteLine($"总单元格数: {totalCells}");
        Console.WriteLine($"已探索单元格: {exploredCells} ({exploredCells * 100.0 / totalCells:F1}%)");
        Console.WriteLine($"已访问单元格: {visitedCells} ({visitedCells * 100.0 / totalCells:F1}%)");
        Console.WriteLine($"路径单元格: {pathCells} ({pathCells * 100.0 / totalCells:F1}%)");
    }
}
