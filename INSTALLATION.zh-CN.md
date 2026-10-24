# 安装与移除

[English](INSTALLATION.md)

使用 Windows x64／CPython 3.12.14（magic `cb0d0d0a`，优化级别0），Python需另行取得。所有命令使用 `-B`，不要加 `-O` 或假定其他解释器兼容。程序和受管理状态共存于 `<用户选择的ONHAND_SKILL_AREA>/OnHandRecallLedger/`。不要覆盖已有产品、生产状态或无关目录。

1. 使用 `Get-FileHash -Algorithm SHA256 -LiteralPath <ZIP路径>` 与另附的 `SHA256SUMS.txt` 对照。完整解包并保留解出的 `OnHandRecallLedger/` 目录。在该目录执行：

   ```powershell
   python -B .\install.py --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA
   python -B C:\OnHandLocal\ONHAND_SKILL_AREA\OnHandRecallLedger\smoke.py --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA
   ```

   示例路径应替换为有权使用的本地位置，末级须为 `ONHAND_SKILL_AREA`。安装逐项校验manifest载荷摘要，拒绝解包源中的额外文件；新建产品home、安装记录及本机绝对目标配置。不复制用户状态，不自动登记Host。首次公开调用初始化根anchor和私有领域。

2. 让Host发现已安装 `SKILL.md`。调用形式为向 `python -B <已安装home>/invoke.py --skill-area <用户选定根>` 的stdin输入一份UTF-8 JSON。字段和合法生命周期见SKILL及两份必读public references。可选 `--current-project` 明确当前项目。`request_digest` 是排除本字段后规范JSON的UTF-8 SHA256：键排序、紧凑分隔、原始Unicode、禁止非有限数；`result_digest`同理核验。`smoke.py`演示设置读取，不提交Knowledge或Recall正文。退出0只是正常状态的传输结果，不保证业务完成。

3. 断开前停止新请求，排空在途工作并核实效果。从Host移除或禁用发现入口；兼容Combined环境通过另装Thoroughfare的合法会话关闭及正式移除机制处理。直接调用 `resident_entry.py` 不构成正式attachment。产品没有daemon，也不自动改Host配置。

4. 完成断开并一致备份状态根后，只移除manifest列出的程序文件：

   ```powershell
   python -B C:\OnHandLocal\ONHAND_SKILL_AREA\OnHandRecallLedger\manage.py uninstall --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA --quiescent --retain-data
   ```

   `--quiescent`是Host声明，须确实先排空调用；既有Core根锁另会拒绝活跃写入者。Knowledge、Recall、barrier、journal、anchor和安装记录保留。完整性不符或不明残留时停止；这不是数据擦除命令。

5. 恢复**同一构件**时，回到保留的完整解包目录执行：

   ```powershell
   python -B .\install.py --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA --restore-program --quiescent
   ```

   要求匹配安装记录、完整anchor、无程序残留；恢复程序与目标配置，不迁移或重置受管理状态。不支持换构件、自动升级或旧格式。遇未知／不完整状态，应停止，不删锁、不补造anchor、不盲目重试。首次安装中途失败会保留这个有界目标供检查，不隐藏部分结果。

内容删除是另一项明确由Host授权的 `erasure.execute` 操作，遵守合同的精确范围与操作身份；PENDING／PARTIAL不是COMPLETE。未知副本、备份和物理介质不在保证范围内。整个数据根的移除须另行核实边界并由用户决定；本工具不提供递归删数据命令。

状态、备份和安装记录须保持私密；分发ZIP只含程序及公开材料，不要转发已经产生状态的安装home。移动盘符须先停用，核实用户提供的根，明确更新绝对目标及Host发现配置，再开新合法会话。自动重定位和跨设备运行未验证。

WSL适配器委托Windows Python及同一Windows根，不是Linux Core；详细参数见SKILL，本构件没有重做WSL互操作测试。新Combined安装须自行满足兼容传输与接线审查，不附带生产Binding或attachment。
