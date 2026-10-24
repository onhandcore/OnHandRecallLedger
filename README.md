# OnHandRecallLedger

English · [简体中文](README.zh-CN.md)

**Reuse useful experience. Build better knowledge through real use.** OnHandRecallLedger is an external Skill that helps a Host avoid repeating past exploration and draw on knowledge tested in actual tasks. It combines two independent lifecycles—Recall and Knowledge—in one Core. The Host decides what the material means, whether it is lawful to retain, and whether it applies now; the Skill enforces contracts and manages state.

Product version **1.0.0**. Windows distribution: **CPython 3.12.14, x64**. Python and other Skills are obtained separately.

## What it does

**Recall** stores experience deliberately admitted by the Host. Admission creates Working items; explicit publication makes them available to bounded retrieval. A historical match is context, not proof of a current fact or permission to act. Recall can reduce repeated exploration when the Host finds the earlier experience relevant.

**Knowledge** accepts candidate claims and Host-supplied evidence from real use. The Skill checks the contract and manages validation, conflicts, revisions, and trust transitions. Candidate does not mean Trusted. The current contract requires three consecutive qualifying PASS outcomes for distinct uses; reads and searches do not validate a claim. Trusted status is checked for expiry on access after seven days, and revised content does not inherit trust. Even Trusted knowledge is supporting material, not current Authority.

The Skill does not reason for the Host, authenticate the truth of submitted evidence, watch conversations, intercept prompts, or silently accumulate every task. Namespace and revision checks provide mechanical isolation, not cryptographic Host authentication. Whether reuse improves a particular task remains a Host judgment.

## Install and make a first call

Use Windows x64 with **CPython 3.12.14**, bytecode magic `cb0d0d0a`, optimization level 0. This build does not promise support for other Python versions, including other 3.12 patch releases. It needs read/write access to the selected local state root and working Windows file locks and atomic file replacement. No extra business library, external API, or API key is required by the inspected runtime; the Host's own models and tools may have separate costs.

Verify the ZIP against its external `SHA256SUMS.txt`, extract it completely, and open PowerShell in the extracted `OnHandRecallLedger` directory. Keep that extracted directory for same-build restoration. Choose a **new** installation root; the final directory name must be `ONHAND_SKILL_AREA`:

```powershell
python -B .\install.py --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA
python -B C:\OnHandLocal\ONHAND_SKILL_AREA\OnHandRecallLedger\smoke.py --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA
```

The first command refuses an existing product home. It copies program files and generates a local `isolated_target.json`; it does not register a Host or a Thoroughfare connection. The second command sends a settings-read request, checks the response digest, and repeats it to check idempotency. It initializes private state, but creates no Recall or Knowledge content. Adjust the example path to a location you own.

For normal use, let the Host discover the installed [SKILL.md](SKILL.md) and read its two required [operation](references/public-contract.json) and [material-request](references/public-material-request.md) references. Send one UTF-8 JSON request on stdin to:

```powershell
python -B C:\OnHandLocal\ONHAND_SKILL_AREA\OnHandRecallLedger\invoke.py --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA
```

`--current-project` is optional. Results are JSON on stdout. Exit 0 includes normal statuses such as PENDING and PARTIAL, so inspect the returned status rather than treating the exit code as completed work. [Installation details](INSTALLATION.md) cover verification, request construction, restoration, and removal.

## Standalone and optional connections

Standalone execution does not require Thoroughfare, Drudge, BestFit, or another Skill. The thin CLI and resident entry delegate to the same Core.

Combined use requires a separately obtained, compatible Thoroughfare and its own valid wiring review and formal registration. The existing deployed combination has prior acceptance evidence; this distribution's resident adapter has an isolated loading check. This is not proof of a new user's first Combined installation. Do not reuse another installation's Binding, line number, or session attachment. This distribution's changed contract bytes need their own wiring review before formal connection.

SESSION_RESIDENT means that a legal attachment is reused within one logical Host session and becomes invalid when that session ends. It is not a background daemon and does not poll, reconnect, or decide to execute work automatically. Host discovery does not guarantee proactive selection.

## Verification and limits

Prior Windows evidence covers the 18-operation surface, source-based Standalone use, the deployed Combined/session-resident path, Recall publication and retrieval, Knowledge state transitions, deletion recovery, and idempotency. That evidence is reused for unchanged Core logic; coverage of an operation name does not mean every successful mutation path was exercised.

This distribution has additional isolated checks for ZIP integrity, bytecode loading, fresh installation, settings-read replay, fixture Candidate/Recall persistence across separate Windows processes, the resident adapter, program removal with data retained, and same-build restoration. Process restart is not a real cross-Host or independently attached logical-session E2E. Knowledge's three-PASS mechanism has prior tests; this build does not claim three real business uses independently validated a claim into Trusted.

Unprompted natural recall, autonomous knowledge capture, other Hosts, clean machines, other Python versions, and cross-device SSD use remain unverified. Native Linux/macOS Core execution is unsupported. The included WSL entry delegates to Windows; WSL interoperation is not revalidated for this bytecode build. Moving a drive can invalidate absolute configuration: stop calls, validate the current location, reconfigure deliberately, and create a fresh legal session. Automatic relocation is not provided. Bytecode does not guarantee resistance to reverse engineering.

## Disconnect, remove, and retain your data

Stop new calls and drain work. For Standalone, remove or disable the Host's discovery entry. For Combined, close the legal Host session and use Thoroughfare's formal removal lifecycle where applicable. There is no daemon to stop.

After disconnecting, remove only the installed program files while retaining managed state:

```powershell
python -B C:\OnHandLocal\ONHAND_SKILL_AREA\OnHandRecallLedger\manage.py uninstall --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA --quiescent --retain-data
```

This does not erase Knowledge, Recall, barriers, recovery records, or the root anchor. Same-build program restoration from the retained extracted directory is described in [INSTALLATION.md](INSTALLATION.md). Automatic upgrades and old-format migrations are not provided. Back up a consistent whole state root, not just knowledge bodies. Content erasure requires an explicit authorized public operation; COMPLETE covers managed surfaces, not unknown copies, backups, or physical SSD erasure. Never delete an entire shared product/data home just to remove its program files.

## License and downloads

The [OnHand Family Closed-Source Distribution License](LICENSE) covers this new first-party distribution. Complete, unmodified official distributions may be freely redistributed. Other rights are governed by the license. Existing lawful MIT grants, independent third-party licenses, and legally reserved rights remain unaffected. Chinese is the governing license text; English is a convenience translation. See [third-party and existing-grant notices](THIRD_PARTY_NOTICES.md).

**Official release:** [OnHandRecallLedger 1.0.0 — downloads and release notes](https://github.com/onhandcore/OnHandRecallLedger/releases/tag/first-public-bilingual-20261024). Download the complete bilingual Windows ZIP and `SHA256SUMS.txt` from the same Release. Both languages describe the same package, version, and hash.
