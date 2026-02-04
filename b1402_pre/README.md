运行说明（b1402_gpt）

本目录包含两个脚本：
- centralityhistograms.py：在原始版本基础上新增 Katz 与 Eigenvector centrality，并为这两种 centrality 额外输出 heat map 与 radar map。
- pagerank_analysis.py：专注计算 PageRank，并输出 histogram/heat map/radar map，同时输出基础统计，并支持按节点查询 PageRank。

数据准备
1) 从 SNAP 下载 twitter_combined.txt.gz：
   https://snap.stanford.edu/data/ego-Twitter.html
2) 解压得到 twitter_combined.txt，并放到脚本同目录，或通过 --input 指定路径。

依赖安装
pip install -r requirements.txt

脚本 1：centralityhistograms.py
- 默认读取无向图（将输入的有向边转为无向）。
- 为了保证运行时间可控：
  - closeness 仍然是对节点做采样（默认 1000 个）
  - betweenness 使用 NetworkX 的 k=1000 采样近似
  - Katz/Eigenvector 可能在全图过慢，因此默认会在“最多 50000 个节点”的诱导子图上计算（可用 --katz-max-nodes 调整）

示例：
python centralityhistograms.py --input twitter_combined.txt
python centralityhistograms.py --input twitter_combined.txt --katz-max-nodes 30000
python centralityhistograms.py --input twitter_combined.txt --force

输出文件（当前目录或 --outdir）：
- degree_c.png
- closeness_c.png
- betweenness_c.png
- katz_c_hist.png / katz_c_heat.png / katz_c_radar.png
- eigenvector_c_hist.png / eigenvector_c_heat.png / eigenvector_c_radar.png

脚本 2：pagerank_analysis.py
- 使用有向图进行 PageRank（与原始边方向一致）。
- 提供两种加速方式，保证 5 分钟内更容易跑完：
  - --edge-sample：按比例随机抽边（例如 0.2）
  - --max-edges：读取边数上限（例如 5000000）

示例：
python pagerank_analysis.py --input twitter_combined.txt
python pagerank_analysis.py --input twitter_combined.txt --edge-sample 0.2
python pagerank_analysis.py --input twitter_combined.txt --max-edges 5000000
python pagerank_analysis.py --input twitter_combined.txt --edge-sample 0.2 --interactive

输出文件：
- pagerank_hist.png
- pagerank_heat.png
- pagerank_radar.png
- pagerank_stats.txt
- pagerank_values.npz（保存 nodes 与 pagerank 数组，便于复现实验与离线查询）
