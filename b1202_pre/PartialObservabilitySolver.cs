using System;
using System.Collections.Generic;

public class PartialObservabilitySolver
{
    private Maze maze;
    private Cell endCell;
    private Dictionary<(int, int), KnownCell> knownMap; // 代理的内部地图
    
    // 内部地图中的单元格信息
    private class KnownCell
    {
        public bool[] Walls = { true, true, true, true }; // 已知的墙壁信息
        public bool[] WallsKnown = { false, false, false, false }; // 哪些墙壁已被探索
        public bool Visited = false; // 是否已访问
        public bool InPath = false; // 是否在解决路径上
    }

    public PartialObservabilitySolver(Maze maze)
    {
        this.maze = maze;
        endCell = maze.GetEndCell();
        knownMap = new Dictionary<(int, int), KnownCell>();
    }

    public bool Solve()
    {
        Cell startCell = maze.GetStartCell();
        // 扫描起始位置
        ScanCell(startCell);
        return DFS(startCell, new HashSet<(int, int)>());
    }

    // 扫描当前单元格的相邻单元格，更新内部地图
    private void ScanCell(Cell cell)
    {
        int x = cell.X;
        int y = cell.Y;
        
        // 标记当前单元格为已探索
        cell.Explored = true;
        
        // 确保当前单元格在已知地图中
        if (!knownMap.ContainsKey((x, y)))
        {
            knownMap[(x, y)] = new KnownCell();
        }
        
        var known = knownMap[(x, y)];
        
        // 扫描四个方向的墙壁
        for (int dir = 0; dir < 4; dir++)
        {
            known.Walls[dir] = cell.Walls[dir];
            known.WallsKnown[dir] = true;
            cell.WallsKnown[dir] = true;
        }
        
        // 扫描相邻单元格的存在性（但不扫描它们的墙壁）
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
            if (nx >= 0 && ny >= 0 && nx < maze.Width && ny < maze.Height)
            {
                // 如果没有墙，我们知道相邻单元格存在
                if (!cell.Walls[wall])
                {
                    if (!knownMap.ContainsKey((nx, ny)))
                    {
                        knownMap[(nx, ny)] = new KnownCell();
                    }
                    
                    // 标记相邻单元格为已探索（至少知道它的存在）
                    Cell neighbor = maze.Grid[nx, ny];
                    neighbor.Explored = true;
                }
            }
        }
    }

    private bool DFS(Cell cell, HashSet<(int, int)> visited)
    {
        int x = cell.X, y = cell.Y;
        visited.Add((x, y));
        
        // 标记为已访问
        if (knownMap.ContainsKey((x, y)))
        {
            knownMap[(x, y)].Visited = true;
        }
        
        // 到达终点
        if (cell == endCell)
        {
            cell.InPath = true;
            if (knownMap.ContainsKey((x, y)))
            {
                knownMap[(x, y)].InPath = true;
            }
            return true;
        }
        
        // 扫描当前位置
        ScanCell(cell);
        
        var directions = new (int dx, int dy, int wall)[]
        {
            (0, -1, 0), // Top
            (1, 0, 1),  // Right
            (0, 1, 2),  // Bottom
            (-1, 0, 3), // Left
        };
        
        // 只使用已知信息进行决策
        foreach (var (dx, dy, wall) in directions)
        {
            int nx = x + dx, ny = y + dy;
            if (nx < 0 || ny < 0 || nx >= maze.Width || ny >= maze.Height)
                continue;
            
            // 使用内部地图的信息
            if (knownMap.ContainsKey((x, y)))
            {
                var known = knownMap[(x, y)];
                
                // 只有当我们知道这个方向没有墙时才尝试移动
                if (known.WallsKnown[wall] && !known.Walls[wall])
                {
                    if (!visited.Contains((nx, ny)))
                    {
                        Cell neighbor = maze.Grid[nx, ny];
                        if (DFS(neighbor, visited))
                        {
                            cell.InPath = true;
                            if (knownMap.ContainsKey((x, y)))
                            {
                                knownMap[(x, y)].InPath = true;
                            }
                            return true;
                        }
                    }
                }
            }
        }
        
        return false;
    }
    
    // 获取已知地图（用于渲染）
    public Dictionary<(int, int), KnownCell> GetKnownMap()
    {
        return knownMap;
    }
    
    // 检查位置是否已被探索
    public bool IsExplored(int x, int y)
    {
        return maze.Grid[x, y].Explored;
    }
    
    // 检查位置是否在路径上
    public bool IsInPath(int x, int y)
    {
        return maze.Grid[x, y].InPath;
    }
}
