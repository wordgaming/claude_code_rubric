using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("Enter maze width:");
        int width = int.Parse(Console.ReadLine());
        Console.WriteLine("Enter maze height:");
        int height = int.Parse(Console.ReadLine());

        Maze maze = new Maze(width, height);
        maze.Generate();
        Console.WriteLine("\nMaze Before Solution\n");
        Renderer.PrintMaze(maze, false);

        Solver solver = new Solver(maze);
        bool solved = solver.Solve();
        
        Console.WriteLine("\nSolved Maze:\n");
        Renderer.PrintMaze(maze, solved);

    }
}