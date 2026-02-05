using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("=== 部分可观察性迷宫求解器 ===");
        Console.WriteLine("该程序演示了在战争迷雾下使用DFS求解迷宫\n");
        
        Console.WriteLine("请输入迷宫宽度:");
        int width = int.Parse(Console.ReadLine() ?? "5");
        Console.WriteLine("请输入迷宫高度:");
        int height = int.Parse(Console.ReadLine() ?? "5");

        // 生成迷宫
        Maze maze = new Maze(width, height);
        maze.Generate();
        
        Console.WriteLine("\n正在生成迷宫...");
        Console.WriteLine("代理将在部分可观察性条件下探索迷宫。");
        Console.WriteLine("代理只能看到相邻的单元格，并逐步构建地图。\n");
        
        // 显示完整迷宫（用于对比）
        Console.WriteLine("按回车键查看完整迷宫（作为参考）...");
        Console.ReadLine();
        PartialRenderer.PrintFullMaze(maze, false);
        
        // 使用部分可观察性求解器
        Console.WriteLine("\n按回车键开始部分可观察性求解...");
        Console.ReadLine();
        
        PartialObservabilitySolver solver = new PartialObservabilitySolver(maze);
        bool solved = solver.Solve();
        
        // 显示求解后的迷宫（带战争迷雾）
        Console.WriteLine("\n求解完成！");
        PartialRenderer.PrintMaze(maze, solver, solved);
        
        // 显示统计信息
        PartialRenderer.PrintStatistics(maze);
        
        // 再次显示完整迷宫以便对比
        Console.WriteLine("\n按回车键查看完整迷宫（对比探索结果）...");
        Console.ReadLine();
        PartialRenderer.PrintFullMaze(maze, solved);
        
        if (solved)
        {
            Console.WriteLine("\n✓ 成功找到从起点到终点的路径！");
            Console.WriteLine("注意：代理仅使用其探索过的信息找到了路径。");
        }
        else
        {
            Console.WriteLine("\n✗ 未找到路径（这不应该发生在完美迷宫中）");
        }
        
        Console.WriteLine("\n按回车键退出...");
        Console.ReadLine();
    }
}
