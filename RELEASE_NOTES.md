# OnHandRecallLedger 1.0.0

[简体中文](RELEASE_NOTES.zh-CN.md)

Distribution identity: `BILINGUAL-C01-20261024-R02-Windows-CPython312`.
Official public release: https://github.com/onhandcore/OnHandRecallLedger/releases/tag/first-public-bilingual-20261024. The approved C01 R02 ZIP is published unchanged; its enclosed documents retain their pre-publication status text. See the GitHub Release for the current publication status and limitations.

The single unchanged Core provides Recall and Knowledge with 18 public operations. The original 17 operations use request/response version 1.0; `host.material.request` uses 1.1 for EVALUATE and SETTLE, with nested material operations remaining 1.0. SETTLE adopts material and its receipt within the owning domain transaction. It does not publish Recall, promote Knowledge or prove semantic correctness.

This build packages first-party implementation as CPython 3.12.14 x64 bytecode, with readable thin entries and installation tools. Source bytes of the Core are unchanged. Bytecode compilation and installation behavior have targeted isolated checks, not a fresh full-domain E2E claim. See the [README](README.md) for tested scope and limitations.

Historical reviews and deployed Combined evidence do not authorize registering a new distribution or copying an existing Binding. This build's documentation, license and packaging edges change contract bytes; a separate bounded wiring review is required before formal Combined registration. Public references retaining earlier candidate-review labels describe their source-contract history, not completed review of this distribution.

The new first-party distribution uses the family closed-source license. Historical MIT material and genuinely existing lawful grants are preserved. Historical source wheels/ZIPs are not this bytecode distribution. Python, its standard library, build tools, Host applications and other Skills are not bundled. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
