# Installation and removal

[简体中文](INSTALLATION.zh-CN.md)

Use Windows x64 / CPython 3.12.14 (`cb0d0d0a`, optimization 0). Obtain Python separately. Run all commands with `-B`; do not use `-O` or assume another interpreter is compatible. The program bundle and managed state coexist at `<chosen ONHAND_SKILL_AREA>/OnHandRecallLedger/`. Do not install over an existing product, production state, or an unrelated directory.

1. Run `Get-FileHash -Algorithm SHA256 -LiteralPath <ZIP path>` and compare with the separately supplied `SHA256SUMS.txt`. Extract the ZIP completely and retain the extracted `OnHandRecallLedger/` directory. From that directory:

   ```powershell
   python -B .\install.py --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA
   python -B C:\OnHandLocal\ONHAND_SKILL_AREA\OnHandRecallLedger\smoke.py --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA
   ```

   Replace the sample path with an owned local path ending in `ONHAND_SKILL_AREA`. Installation checks every manifest-listed payload hash and refuses extra files in the extracted source. It creates a fresh product home, an installation record and an absolute local target configuration. It does not copy user state or register a Host. First public use initializes the root anchor and private domains.

2. Let the Host discover the installed `SKILL.md`. A call is one UTF-8 JSON request on stdin to `python -B <installed home>/invoke.py --skill-area <chosen root>`. Read `SKILL.md` and both required public references for fields and permitted lifecycle operations. An optional `--current-project` specifies the current project. Compute `request_digest` as SHA256 of UTF-8 JSON excluding that field, with sorted keys, compact separators, literal Unicode and no nonfinite numbers. Verify `result_digest` in the same way. `smoke.py` demonstrates a settings read without submitting Knowledge or Recall content. Exit 0 is a normal-status transport result, not a promise of business completion.

3. To disconnect, stop new requests, wait for in-flight work and verify effects. Disable/remove the discovery entry in the Host. A compatible Combined setup must use the legal session close and formal removal mechanisms of its separately installed Thoroughfare. A direct call to `resident_entry.py` is not formal attachment. No daemon exists and no automatic Host configuration is performed.

4. After disconnecting and backing up a consistent state root, remove only manifest-listed program files:

   ```powershell
   python -B C:\OnHandLocal\ONHAND_SKILL_AREA\OnHandRecallLedger\manage.py uninstall --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA --quiescent --retain-data
   ```

   `--quiescent` is a Host declaration: actually drain calls first. The existing Core root lock additionally refuses an active writer. Knowledge, Recall, barriers, journals, the anchor and an installation record remain. Program integrity failures or unknown residue stop the operation. This is not a data eraser.

5. To restore this **same artifact**, return to the retained, complete extracted directory and run:

   ```powershell
   python -B .\install.py --skill-area C:\OnHandLocal\ONHAND_SKILL_AREA --restore-program --quiescent
   ```

   It requires the matching installation record, intact anchor, and absence of program residue. It restores program files and target configuration without migrating or resetting managed state. It does not support another artifact, automatic upgrades or old formats. On unknown/partial state, stop rather than deleting locks, recreating anchors or blindly retrying. If an installation fails partway, keep that bounded destination for inspection; the tool does not hide the partial result.

Content deletion is a separate explicit Host-authorized `erasure.execute` operation. Follow the public contract, exact scope and operation identity; PENDING/PARTIAL are not COMPLETE. Unknown copies, backups and physical media are outside its guarantee. Full data-root removal requires a separately verified boundary and user decision; these tools provide no recursive data deletion command.

Keep state, backups and installation records private. The distributed ZIP contains program and public materials only. Do not redistribute an installed home containing state. Drive relocation is manual: quiesce, verify the user-supplied root, deliberately update the absolute target and Host discovery, then open a fresh legal session. Automatic relocation and cross-device operation are not verified.

The WSL adapter delegates to Windows Python and the same Windows root; it is not a Linux Core. Its detailed arguments remain in `SKILL.md`; this build has not repeated WSL interoperation tests. New Combined installations require their own compatible transport and wiring review; no production Binding or attachment is included.
