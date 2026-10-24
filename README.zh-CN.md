# OnHandRecallLedger

[English](README.md) · 简体中文

**复用有价值的经验，让知识在真实使用中得到验证。** OnHandRecallLedger 是一款外置 Skill：Recall 帮助 Host 减少重复探索，Knowledge 通过真实任务中的使用验证，为未来任务提供更可靠的参考。两条独立价值生命周期共用一个 Core。Host 负责语义理解、合法保留与当前适用性判断；Skill 负责合同校验和状态管理。

产品版本 **1.0.0**。Windows 发行范围：**CPython 3.12.14，x64**。Python 和其他 Skill 需另行取得。

## 核心能力与责任边界

**Recall** 保存 Host 明确选择准入的历史经验。准入产生 Working，只有显式合法发布后，才进入有界检索范围。历史命中只是参考，不是当前事实的证明，也不授予执行权限。Host 判断经验适用时，复用才可能减少重复探索。

**Knowledge** 接收候选知识和 Host 提交的真实使用证据，校验合同并管理验证、冲突、修订与信任状态。Candidate 不等于 Trusted。当前合同要求三次连续、合格且不重复的使用 PASS；读取和搜索不算验证。Trusted 在访问时按七日期限检查过期，内容修订不继承信任。即使 Trusted，也只是支持材料，不是当前 Authority。

产品不会代替 Host 推理、判断证据真伪、监视会话、拦截提示词或无条件沉淀所有任务。命名空间和版本检查是机械隔离，不是密码学 Host 身份认证。具体任务是否因此改善，仍由 Host 判断。

## 安装与首次调用

使用 Windows x64 与 **CPython 3.12.14**，字节码 magic 为 `cb0d0d0a`，优化级别为 0。本构件不承诺支持其他 Python 版本，包括其他 3.12 补丁版。选定的本地状态根需要合法读写权限，并支持 Windows 文件锁和原子替换。检查范围内的运行时不需要额外业务库、外部 API 或 API Key；Host 自身模型和工具可能另有费用。

先以外部 `SHA256SUMS.txt` 核验 ZIP，完整解包，在解出的 `OnHandRecallLedger` 目录打开 PowerShell。保留这个解包目录供同构件恢复使用。选择一个**全新**安装根，末级目录必须名为 `ONHAND_SKILL_AREA`：

```powershell
python -B .\install.py --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA
python -B C:\OnHandLocal\ONHAND_SKILL_AREA\OnHandRecallLedger\smoke.py --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA
```

第一条命令拒绝已有产品 home，只复制程序并生成本机 `isolated_target.json`，不会自动登记 Host 或 Thoroughfare 连接。第二条命令发送设置读取请求，核验响应摘要并重复请求检查幂等；它会初始化私有状态，但不创建 Recall 或 Knowledge 内容。示例路径请换成用户有权使用的位置。

日常使用时，让 Host 发现已安装的 [SKILL.md](SKILL.md)，并阅读必需的[操作清单](references/public-contract.json)和[材料请求合同](references/public-material-request.md)。向以下入口的 stdin 提交一份 UTF-8 JSON：

```powershell
python -B C:\OnHandLocal\ONHAND_SKILL_AREA\OnHandRecallLedger\invoke.py --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA
```

可选 `--current-project`；stdout 返回 JSON。退出码 0 也涵盖 PENDING、PARTIAL 等正常状态，应检查实际返回状态，不能只据退出码判断任务已完成。校验、请求构造、恢复和移除步骤见[安装说明](INSTALLATION.zh-CN.md)。

## 独立运行与可选组合

Standalone 独立运行不需要 Thoroughfare、Drudge、BestFit 或其他 Skill。薄 CLI 与 resident 入口委托同一个 Core。

Combined 需另行取得兼容的 Thoroughfare，并完成自身合法接线审查和正式登记。既有现役组合已有验收证据；本构件的 resident 适配器另做了隔离加载检查。这不等于新用户首次 Combined 安装已经通过。不得复用其他安装的 Binding、线路编号或会话 attachment。本构件合同字节已变化，正式连接前须单独完成相应接线审查。

SESSION_RESIDENT 表示在一个合法逻辑 Host 会话内复用 attachment，会话结束后失效；它不是后台守护进程，不轮询、不自动重连，也不自行决定执行任务。Host 能发现入口不代表会主动选择它。

## 验证范围与限制

已有 Windows 证据覆盖 18-operation 公共面、源码 Standalone、现役 Combined／会话驻留路径、Recall 发布检索、Knowledge 状态转换、删除恢复及幂等。本构件复用未改动 Core 的这些证据；覆盖操作名称不等于每个成功修改路径都已验过。

本构件另有隔离检查：ZIP 完整性、字节码加载、首次安装、设置读取重试、测试 Candidate／Recall 在独立 Windows 进程间持久读取、resident 适配器、保留数据的程序卸载及同构件恢复。重启进程不等于真实跨 Host 或独立 attachment 的逻辑会话 E2E。知识三次 PASS 机制已有测试，但本构件不声称完成了将知识晋升 Trusted 的三次真实业务使用独立验收。

无提示自然召回、自主知识沉淀、其他 Host、干净机器、其他 Python 版本及跨设备 SSD 仍未验证。Linux／macOS 原生 Core 不支持；所附 WSL 入口委托 Windows，本次字节码构件没有重新验证 WSL 互操作。移动盘符可能使绝对配置失效：先停用，核实当前位置，明确重新配置，再建立新的合法会话；不提供自动重定位。字节码不保证不可逆向。

## 断开、卸载与数据保留

停止新请求并排空在途工作。Standalone 从 Host 自身配置移除或禁用发现入口；Combined 结束合法 Host 会话，并在需要时走 Thoroughfare 正式移除流程。没有要停止的后台 daemon。

完成断开后，只移除安装程序文件、保留受管理状态：

```powershell
python -B C:\OnHandLocal\ONHAND_SKILL_AREA\OnHandRecallLedger\manage.py uninstall --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA --quiescent --retain-data
```

此命令不擦除 Knowledge、Recall、barrier、恢复记录或根 anchor。使用保留的解包目录恢复同构件程序，见 [INSTALLATION.zh-CN.md](INSTALLATION.zh-CN.md)。不提供自动升级或旧格式迁移。备份应保留一致的完整状态根，不能只留知识正文。内容清理需明确授权的公开操作；COMPLETE 仅覆盖受管理表面，不保证未知副本、备份或 SSD 物理擦除。不要为了移除程序而递归删除共存数据的整个 home。

## 许可与下载

本次新发行第一方成品适用 [OnHand 家族闭源发行许可](LICENSE)，允许自由转发官方完整、未经修改的成品；其他权利以许可条文为准。既有合法 MIT 授权、独立第三方许可和法律保留权利不受影响。中文为适用许可正文，英文仅为便利翻译。参见[第三方与既有授权说明](THIRD_PARTY_NOTICES.md)。

**正式发行：** [OnHandRecallLedger 1.0.0 下载与发行说明](https://github.com/onhandcore/OnHandRecallLedger/releases/tag/first-public-bilingual-20261024)。从同一 Release 下载完整双语 Windows ZIP 和 `SHA256SUMS.txt`。中英文对应同一产品包、版本和摘要。
