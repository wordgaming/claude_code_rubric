# 部分可观察性迷宫求解器 - 设计文档

## 设计目标

将原始的完全可观察DFS迷宫求解器改造为部分可观察性版本，实现以下核心要求：

1. **部分可观察性**: 代理只能感知相邻单元格
2. **动态地图构建**: 逐步构建内部地图
3. **战争迷雾**: 可视化未探索区域
4. **基于已知信息决策**: 不依赖完整迷宫数据

## 架构设计

### 1. 数据结构设计

#### Cell类增强
```csharp
public class Cell
{
    // 原有属性
    public int X, Y;
    public bool Visited = false;
    public bool[] Walls = { true, true, true, true };
    public bool InPath = false;
    
    // 新增属性
    public bool Explored = false;              // 是否已被探索
    public bool[] WallsKnown = { false, false, false, false }; // 墙壁是否已知
}
```

**设计理由**:
- `Explored`: 标记单元格是否被代理扫描过
- `WallsKnown`: 跟踪每面墙是否已被探索，支持部分信息

#### 内部地图结构
```csharp
private class KnownCell
{
    public bool[] Walls = { true, true, true, true };
    public bool[] WallsKnown = { false, false, false, false };
    public bool Visited = false;
    public bool InPath = false;
}

private Dictionary<(int, int), KnownCell> knownMap;
```

**设计理由**:
- 使用独立的数据结构存储代理的知识
- 与真实迷宫数据分离，确保不会"作弊"
- 使用坐标元组作为键，高效查找

### 2. 核心算法设计

#### 扫描机制 (ScanCell)

```
算法: ScanCell(cell)
输入: 当前单元格
输出: 更新内部地图

1. 标记当前单元格为已探索
2. 如果单元格不在内部地图中，创建新条目
3. 扫描四个方向的墙壁:
   - 读取真实墙壁信息
   - 更新内部地图的墙壁信息
   - 标记墙壁为已知
4. 对于每个没有墙的方向:
   - 确保相邻单元格在内部地图中存在
   - 标记相邻单元格为已探索
```

**关键点**:
- 只在当前位置扫描，不远程探测
- 相邻单元格只标记存在，不扫描其墙壁
- 保持部分可观察性的约束

#### DFS求解算法

```
算法: DFS(cell, visited)
输入: 当前单元格, 已访问集合
输出: 是否找到路径

1. 将当前单元格加入已访问集合
2. 标记内部地图中的单元格为已访问
3. 如果到达终点:
   - 标记为路径的一部分
   - 返回true
4. 扫描当前单元格 (ScanCell)
5. 对于四个方向:
   - 检查是否在边界内
   - 从内部地图获取墙壁信息
   - 如果墙壁已知且没有墙:
     - 如果相邻单元格未访问:
       - 递归调用DFS
       - 如果找到路径，标记当前单元格为路径
6. 返回false
```

**关键点**:
- 先扫描再决策
- 只使用内部地图的信息
- 不访问真实迷宫的墙壁信息（除了扫描时）

### 3. 渲染设计

#### 战争迷雾渲染

```
算法: PrintMaze(maze, solver, solved)

对于每个单元格(x, y):
  如果未探索:
    显示迷雾符号 ░
  否则:
    如果墙壁已知:
      显示墙壁 #
    否则:
      显示迷雾 ░
    
    显示单元格内容:
      - S: 起点
      - E: 终点
      - ?: 路径
      - ·: 已访问
      - 空格: 未访问
```

**视觉设计**:
- `░` (迷雾) - 未探索区域
- `#` (墙壁) - 已知的墙
- `?` (路径) - 解决方案路径
- `·` (点) - 已访问但不在路径上
- `S/E` - 起点/终点

### 4. 信息流设计

```
真实迷宫 (Maze.Grid)
    ↓ (仅在扫描时读取)
扫描机制 (ScanCell)
    ↓ (更新)
内部地图 (knownMap)
    ↓ (查询)
决策机制 (DFS)
    ↓ (移动)
新位置
    ↓ (循环)
```

**关键约束**:
- DFS不直接访问Maze.Grid的墙壁信息
- 所有决策基于knownMap
- 只在ScanCell时读取真实数据

## 实现细节

### 1. 部分可观察性的实现

**问题**: 如何确保代理不"作弊"？

**解决方案**:
1. 维护独立的内部地图
2. DFS只查询内部地图
3. 只在扫描时更新内部地图
4. 使用WallsKnown数组跟踪已知信息

**验证**:
```csharp
// 错误做法（作弊）
if (!cell.Walls[wall]) { ... }

// 正确做法（使用内部地图）
if (known.WallsKnown[wall] && !known.Walls[wall]) { ... }
```

### 2. 渐进式地图构建

**挑战**: 如何逐步构建地图？

**实现**:
```csharp
// 第一次访问时创建条目
if (!knownMap.ContainsKey((x, y)))
{
    knownMap[(x, y)] = new KnownCell();
}

// 扫描时更新信息
known.Walls[dir] = cell.Walls[dir];
known.WallsKnown[dir] = true;
```

### 3. 战争迷雾渲染

**挑战**: 如何区分未探索和已探索区域？

**实现**:
```csharp
if (!cell.Explored)
{
    Console.Write("░░"); // 迷雾
}
else
{
    // 显示已知信息
    if (cell.WallsKnown[0])
        Console.Write(cell.Walls[0] ? "##" : "# ");
    else
        Console.Write("░░"); // 部分迷雾
}
```

### 4. 探索效率

**度量指标**:
- 探索率 = 已探索单元格 / 总单元格
- 访问率 = 已访问单元格 / 总单元格
- 路径效率 = 路径长度 / 最短路径长度

**实现**:
```csharp
public static void PrintStatistics(Maze maze)
{
    int exploredCells = 0;
    for (int x = 0; x < maze.Width; x++)
        for (int y = 0; y < maze.Height; y++)
            if (maze.Grid[x, y].Explored) exploredCells++;
    
    Console.WriteLine($"已探索: {exploredCells} ({exploredCells * 100.0 / totalCells:F1}%)");
}
```

## 算法复杂度分析

### 时间复杂度
- **扫描**: O(1) - 固定4个方向
- **DFS**: O(V + E) - V是顶点数，E是边数
- **总体**: O(V + E) - 与完全可观察版本相同

### 空间复杂度
- **内部地图**: O(V) - 最多存储所有单元格
- **访问集合**: O(V) - DFS栈
- **总体**: O(V)

### 探索效率
- **最好情况**: 直接找到路径，探索率 ≈ 路径长度 / 总单元格
- **最坏情况**: 探索所有可达单元格，探索率 ≈ 100%
- **平均情况**: 取决于迷宫结构和DFS的随机性

## 与原始版本的对比

| 方面 | 原始版本 | 部分可观察性版本 |
|------|---------|-----------------|
| **数据访问** | 直接访问Maze.Grid | 通过knownMap间接访问 |
| **决策依据** | 完整墙壁信息 | 仅已知墙壁信息 |
| **内存使用** | O(V) | O(V) + 内部地图 |
| **时间复杂度** | O(V + E) | O(V + E) + 扫描开销 |
| **可视化** | 显示完整迷宫 | 显示战争迷雾 |
| **真实性** | 不现实（全知） | 更真实（受限感知） |

## 扩展设计

### 1. 可调节的感知范围
```csharp
private void ScanCell(Cell cell, int range)
{
    // 扫描range范围内的单元格
    for (int dx = -range; dx <= range; dx++)
        for (int dy = -range; dy <= range; dy++)
            // 扫描逻辑
}
```

### 2. 不确定性传感器
```csharp
private bool ScanWall(Cell cell, int direction)
{
    bool actualWall = cell.Walls[direction];
    // 添加噪声
    if (random.NextDouble() < errorRate)
        return !actualWall;
    return actualWall;
}
```

### 3. 动画演示
```csharp
private bool DFS(Cell cell, HashSet<(int, int)> visited)
{
    // 每步后渲染
    PartialRenderer.PrintMaze(maze, this, false);
    Thread.Sleep(100); // 延迟
    // 继续DFS
}
```

### 4. 多种算法
- BFS部分可观察性版本
- A*部分可观察性版本
- 贪心算法版本

## 测试策略

### 1. 功能测试
- [ ] 能否找到路径
- [ ] 是否只使用已知信息
- [ ] 战争迷雾是否正确显示

### 2. 边界测试
- [ ] 1x1迷宫
- [ ] 大型迷宫 (100x100)
- [ ] 狭长迷宫 (1xN, Nx1)

### 3. 正确性验证
- [ ] 路径是否连续
- [ ] 是否到达终点
- [ ] 未探索区域是否真的未访问

### 4. 性能测试
- [ ] 不同尺寸的运行时间
- [ ] 内存使用情况
- [ ] 探索效率统计

## 总结

本设计实现了一个真正的部分可观察性迷宫求解器：

✅ **部分可观察性**: 通过独立的内部地图和扫描机制实现
✅ **动态地图构建**: 使用Dictionary动态添加已知单元格
✅ **战争迷雾**: 通过Explored和WallsKnown标志实现
✅ **基于已知信息决策**: DFS只查询内部地图
✅ **可视化**: 清晰显示探索过程和未知区域
✅ **可扩展**: 易于添加新功能和算法

该设计在保持DFS核心逻辑的同时，成功引入了部分可观察性约束，使求解器更接近真实世界的探索场景。
