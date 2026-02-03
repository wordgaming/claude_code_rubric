using System;
using System.Collections.Generic;

public class Maze
{
    public int Width, Height;
    public Cell[,] Grid;
    private Random rnd = new Random();

    public Maze(int width, int height)
    {
        Width = width;
        Height = height;
        Grid = new Cell[width, height];
        for (int x = 0; x < width; x++)
            for (int y = 0; y < height; y++)
                Grid[x, y] = new Cell(x, y);
    }

    public void Generate()
    {
        GenerateMazeFrom(Grid[0, 0]);
    }

    private void GenerateMazeFrom(Cell current)
    {
        current.Visited = true;

        foreach (Cell neighbor in GetShuffledNeighbors(current))
        {
            if (!neighbor.Visited)
            {
                RemoveWall(current, neighbor);
                GenerateMazeFrom(neighbor);
            }
        }
    }

    private List<Cell> GetShuffledNeighbors(Cell cell)
    {
        var list = new List<Cell>();
        int x = cell.X;
        int y = cell.Y;

        if (y > 0) list.Add(Grid[x, y - 1]);     // Top
        if (x < Width - 1) list.Add(Grid[x + 1, y]); // Right
        if (y < Height - 1) list.Add(Grid[x, y + 1]); // Bottom
        if (x > 0) list.Add(Grid[x - 1, y]);     // Left

        for (int i = 0; i < list.Count; i++)
        {
            int j = rnd.Next(i, list.Count);
            var temp = list[i];
            list[i] = list[j];
            list[j] = temp;
        }

        return list;
    }

    private void RemoveWall(Cell a, Cell b)
    {
        int dx = b.X - a.X;
        int dy = b.Y - a.Y;

        if (dx == 1) { a.Walls[1] = false; b.Walls[3] = false; } // a right
        else if (dx == -1) { a.Walls[3] = false; b.Walls[1] = false; } // a left
        else if (dy == 1) { a.Walls[2] = false; b.Walls[0] = false; } // a bottom
        else if (dy == -1) { a.Walls[0] = false; b.Walls[2] = false; } // a top
    }

    public Cell GetStartCell() => Grid[0, 0];
    public Cell GetEndCell() => Grid[Width - 1, Height - 1];
}
