Maze Generator & Solver – C# Console Application
================================================

Overview
-----------
This is a self-contained C# console application that generates a random maze and solves it using depth-first search. 
The solution path is displayed using '?' symbols, clearly connecting cells in all directions.

The application uses only 5 C# source files and has no external dependencies. It can be run via Visual Studio 2022 or from the terminal using the .NET SDK.

🛠 Files
--------
- Program.cs      → Entry point; handles user input and program flow
- Maze.cs         → Generates a perfect maze using recursive backtracking
- Cell.cs         → Represents each maze cell (walls, path flags, etc.)
- Solver.cs       → Solves the maze using DFS and marks the solution path
- Renderer.cs     → Renders the maze as ASCII art in the terminal

How to Run (Option 1: Visual Studio)
--------------------------------------
1. Open the folder containing the 5 .cs files in Visual Studio 2022.
2. Create a new Console App project and add these files to it.
3. Set `Program.cs` as the startup file (should be automatic).
4. Click Run or press F5.

How to Run (Option 2: Terminal)
----------------------------------
1. Make sure the .NET SDK is installed (`dotnet --version` to check).
2. Open a terminal and navigate to the folder with your files.
3. Compile and run using:

   Option A (temporary project):
   > dotnet new console -n MazeApp
   > cd MazeApp
   > copy ..\*.cs .
   > dotnet run

   Option B (manual compile):
   > csc *.cs
   > Program.exe

Usage Instructions
---------------------
1. When prompted, enter the maze width (e.g., 10).
2. Then enter the maze height (e.g., 10).
3. The maze will be generated and solved.
4. Output will show:
   - `#` for walls
   - `S` for the start (top-left)
   - `E` for the end (bottom-right)
   - `?` for the solution path

Notes
--------
- Maze paths may appear visually broken without vertical bridges. 
