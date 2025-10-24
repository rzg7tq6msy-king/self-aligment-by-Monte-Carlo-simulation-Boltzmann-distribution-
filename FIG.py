import pandas as pd
import matplotlib.pyplot as plt
import os

#-------------------------------- 自定义 -----------------------------------
file_path = '/Users/25015/OneDrive/Documents/pattern/simulate/T2T_M1/RUN_log.xlsx'
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names

#------------------------------- 自定义保存路径 ---------------------------
save_dir = "C:/Users/25015/OneDrive/Documents/pattern/simulate/T2T_M1"
os.makedirs(save_dir, exist_ok=True)

fig, axes = plt.subplots(len(sheet_names), 1, figsize=(8, 5*len(sheet_names)), constrained_layout=False)
# 调整边距
# ------------------ 明显增加留白 ------------------
fig.subplots_adjust(
    left=0.15,    # 左边距 15%
    right=0.95,   # 右边留白 15%
    top=0.95,     # 顶部 92%
    bottom=0.05,  # 底部 8%
    hspace=0.5    # 子图之间垂直间距
)

if len(sheet_names) == 1:
    axes = [axes]

for ax, sheet_name in zip(axes, sheet_names):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # 动态列名
    energy_col = f"{sheet_name}_energy"
    energies = df[energy_col]
    
    # 归一化
    norm_energies = [e / 3154 for e in energies]
    
    # 计算百分比
    percentage = round(sum(e <= -0.85 for e in norm_energies) / len(norm_energies) * 100, 2)
    print(f"{sheet_name}: {percentage}%")
    
    # 绘制直方图
    hist_values, bins, _ = ax.hist(norm_energies, bins=50, range=(-1, 0),
                                   color='skyblue', edgecolor='black')
    
    # 将直方图高度转换为百分比
    hist_values_percent = hist_values / hist_values.sum() * 100
    ax.clear()  # 清除之前的直方图
    ax.bar(bins[:-1], hist_values_percent, width=bins[1]-bins[0], color='skyblue', edgecolor='black')
    
    ax.set_ylim(0, 100)
    
    ax.grid(True, linestyle="--", alpha=0.7)

    # 在图上加 sheet name + percentage
    ax.text(-0.85, 85, f"{sheet_name}  {percentage}%", fontsize=16, color='red', ha='center')
   
    
# 整个 figure 的总标题和横纵坐标
fig.suptitle("Energy Distributions", fontsize=24)
fig.text(0.5, 0.01, "Normalized Energy", ha='center', fontsize=24)
fig.text(0.025, 0.5, "Frequency (%)", va='center', rotation='vertical', fontsize=24)

# 保存整列直方图
plt.savefig(os.path.join(save_dir, "All_sheets_histograms.png"))
plt.show()
