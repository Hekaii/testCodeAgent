# testCodeAgent

这是一个用于测试 AI 平台闭环的超轻量伪训练仓库。

特性：

- 纯 Python 标准库，无额外依赖
- `baseline` 模式输出较低指标，触发平台进入下一轮
- `train` 模式输出达标指标，验证闭环能够成功结束
- 训练只会打印少量日志并写出 `metrics.json`

本仓库用于验证：

- 代码 checkout
- 准备命令执行
- 基线运行
- 指标解析
- 计划生成
- patch / validate / train
- 达标判断与总结报告

