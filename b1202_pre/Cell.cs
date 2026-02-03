public class Cell
{
    public int X, Y;
    public bool Visited = false;
    public bool[] Walls = { true, true, true, true }; // Top, Right, Bottom, Left
    public bool InPath = false;

    public Cell(int x, int y)
    {
        X = x;
        Y = y;
    }
}
