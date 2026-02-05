public class Cell
{
    public int X, Y;
    public bool Visited = false;
    public bool[] Walls = { true, true, true, true }; // Top, Right, Bottom, Left
    public bool InPath = false;
    
    // 部分可观察性相关属性
    public bool Explored = false;  // 是否已被探索（扫描过）
    public bool[] WallsKnown = { false, false, false, false }; // 每面墙是否已知
    
    public Cell(int x, int y)
    {
        X = x;
        Y = y;
    }
}
