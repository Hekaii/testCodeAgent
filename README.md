# testCodeAgent

这是一个专门为 AIRunning 阶段性测试准备的“仿真论文训练仓库”。

它不依赖第三方机器学习框架，但目录结构、启动方式和产物组织方式都尽量贴近真实论文代码仓库，方便你测试：

- 通过 SSH 拉取固定版本代码
- 配置固定启动脚本和固定输出文件
- 基线 / 工作区重建
- allowlist 允许编辑范围
- 后续 AI 阅读代码、修改代码、重新训练和查看结果

## 推荐在 AIRunning 中填写的固定配置

- 固定启动脚本：`scripts/run_experiment.py`
- 固定输出文件：`outputs/reports/final_metrics.csv`

建议的启动命令示例：

```bash
python scripts/run_experiment.py --mode train
```

如果你想先跑一个“基线较差、便于后续优化”的版本，可以执行：

```bash
python scripts/run_experiment.py --mode baseline
```

## 仓库结构

```text
configs/
  experiment.json              # 实验超参数和数据文件配置
data/
  raw/
    train.csv                  # 训练集模拟数据
    dev.csv                    # 验证集模拟数据
    test.csv                   # 测试集模拟数据
logs/
  .gitkeep
outputs/
  reports/
    .gitkeep
scripts/
  run_experiment.py            # 固定启动脚本，适合 AIRunning 配置
  run_experiment.ps1           # Windows 包装脚本
  run_experiment.sh            # Linux 包装脚本
train/
  __init__.py
  config_loader.py             # 读取实验配置
  dataset_reader.py            # 读取 CSV 数据
  feature_pipeline.py          # 模拟特征构建
  pseudo_model.py              # 伪模型与指标生成逻辑
  trainer.py                   # 训练过程编排
  reporting.py                 # 输出日志、CSV、JSON 结果
  train.py                     # 训练主入口
project.yaml                   # 平台项目描述
```

## 这个仓库模拟了哪些“真实论文代码”特征

- 有 `data/` 数据目录，区分 `train / dev / test`
- 有 `configs/` 实验配置文件
- 有 `train/` 多模块训练代码，而不是单文件脚本
- 有固定 `scripts/` 启动入口
- 训练后会输出：
  - `outputs/reports/final_metrics.csv`
  - `outputs/reports/epoch_metrics.csv`
  - `outputs/reports/run_summary.json`
  - `logs/train.log`

## 运行效果

- `baseline` 模式会输出一个偏低但合理的分数，方便平台触发“继续优化”
- `train` 模式会输出一个更高的分数，模拟优化成功后的结果
- 整个流程会读取数据、计算特征、记录 epoch 日志、落盘最终指标

## 本地快速测试

```bash
python scripts/run_experiment.py --mode baseline
python scripts/run_experiment.py --mode train
```

运行完成后，重点查看：

- `outputs/reports/final_metrics.csv`
- `logs/train.log`

## 推荐的 allowlist 示例

如果你想在 AIRunning 中只允许 AI 修改训练逻辑，可以考虑先选这些路径：

```text
train/**
configs/**
scripts/run_experiment.py
```

如果你想进一步限制，只允许改模型部分，也可以缩小到：

```text
train/pseudo_model.py
train/trainer.py
configs/experiment.json
```
