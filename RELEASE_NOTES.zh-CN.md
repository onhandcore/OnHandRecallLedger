# OnHandRecallLedger 1.0.0

[English](RELEASE_NOTES.md)

构件身份：`BILINGUAL-C01-20261024-R02-Windows-CPython312`。正式公开发行：https://github.com/onhandcore/OnHandRecallLedger/releases/tag/first-public-bilingual-20261024。已批准的 C01 R02 ZIP 原样发布；包内文档保留发布前状态文字，实际发行状态与限制以本次 GitHub Release 为准。

同一个未改动Core提供Recall与Knowledge，共18项公共操作。原17项使用请求／响应1.0；`host.material.request`的EVALUATE／SETTLE使用1.1，嵌套材料操作仍为1.0。SETTLE在所属领域事务内采用材料并保存回执，不自动发布Recall、晋升Knowledge，也不证明语义正确。

本构件以CPython 3.12.14 x64字节码交付第一方实现，并保留可读薄入口及安装工具。Core源字节未变。编译与安装行为经过针对性的隔离检查，不宣称重新完成全领域E2E；验证范围及限制见[README](README.zh-CN.md)。

历史审查与现役Combined证据不授权登记新构件或复制已有Binding。本构件文档、许可及包装边缘改变了合同字节，正式Combined登记前仍需单独的有界接线审查。公共引用中保留的早期待审标签说明源合同的历史阶段，不代表本构件已完成该审查。

本次新第一方成品适用家族闭源许可，历史MIT材料及真实存在的合法授权保留。旧源码wheel／ZIP不是本次字节码发行包。不捆绑Python、标准库、构建工具、Host或其他Skill，详见[LICENSE](LICENSE)与[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
