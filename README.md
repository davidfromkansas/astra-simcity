# Astra City Observatory

Public dashboard: https://davidfromkansas.github.io/astra-simcity/

Original SimCity 2000 in a separate, locally patched DOSBox-X. This repository contains the public dashboard, city statistics, game screenshots and the public activity journal, not the copyrighted game or emulator runtime.

## Challenge
Reach 2,000 residents before January 1910, then verify three consecutive full years with positive operating budgets. No bonds, money cheats, save-file edits or rewinds during the attempt. Construction expenses are distinguished from annual operating budgets. An attempted challenge may fail; observations are retained honestly.

## Data
`metrics.py` is a read-only IFF/RLE SC2 parser based on the OpenCity2k format documentation. It validates chunk bounds and completed saves. Current population, funds, bonds and workforce are MISC fields. Monthly statistics come from the newest entry of each original XGRP graph. Native graph units are preserved; fields with uncertain semantics are not promoted to invented precise measurements. Annual income/spending are entered only when verified from a year-end budget screen. Missing values display as dashes.

`play.py ACTION JSON REASON` logs a concise public decision, executes one controller action, then logs its result. `sample` saves via the visible File menu and dismisses the confirmation before parsing. Use it from this repository's parent workspace. The game must be on its ordinary city screen. Failed or incomplete saves must be resolved before taking another sample.

`telemetry.py` exports `docs/data.json`. `publisher.py` commits and pushes observations every 300 seconds for a bounded four-hour session; GitHub Pages adds deployment latency. It does not run the game or make decisions. Run only one publisher. The local Mac and its network connection must remain available. The static page polls published JSON every 30 seconds and marks updates older than 15 minutes as delayed.

The sibling bridge recorder records only the game's framebuffer at 5 fps to a recoverable fragmented MP4, with no audio, for up to four hours. It snapshots every 300 seconds; milestone snapshots are also recorded. Its PID and video path are in `../bridge/recordings/session.json`. Send SIGTERM to that verified recorder PID to finalize gracefully. The game remains paused between control actions. No autonomous model loop is hidden in the publisher or recorder.

## Checks
`PYTHONPYCACHEPREFIX=/tmp/astra-pycache python3 test_telemetry.py`

`node --check docs/app.js`

Browser checks: public page loaded; timeline Play advances images; Latest returns to the newest image; chart selector switches the plotted metric.

## Completed first attempt

- Population target verified from the saved city: **2,020 in December 1908**, before the January 1910 deadline.
- Three consecutive full post-target fiscal years: **1909 +$189; 1910 +$191; 1911 +$202**, as displayed in the year-end budget screens. Individual income/spending rows and treasury settlements can differ by $1 due to the game's rounding; the dashboard preserves the displayed totals.
- Final saved state: **January 1912, 2,450 population, $12,796 treasury, zero bonds/debt**.
- 40 screenshots, including regular five-minute captures and milestone/budget evidence. Read-only samples and the public decision/action feed are in `docs/data.json`.
- Silent recordings: `docs/recordings/full-session.mp4` (31m 45.6s, 5 fps) and `docs/recordings/timelapse.mp4` (95.3s, 20× speed).
- The game is paused, and the recording and periodic publisher were stopped after completion. The published dashboard remains available as a replay/archive. Future play requires restarting the local recorder/publisher.
- This is a basic growth-and-budget challenge, not an optimized city: the final game reports crime 34, pollution 102, health 58 and education 83 in their native graph units; public services still need attention.

Six telemetry/scoring checks pass, including rejection of incomplete saves, consecutive-year accounting, and duplicate-year rejection. Both MP4s were probed as valid H.264 at 640×480.
