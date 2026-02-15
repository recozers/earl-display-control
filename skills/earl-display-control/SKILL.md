---
name: earl-display-control
description: Keep the VisuoSpatial Sketchpad (Earl's TV dashboard) online by restarting the local python server, relaunching the Edge kiosk, and editing earl_mind.json through the EarlMind helpers. Use whenever Telegram asks to wake Earl, when the TV shows "Earl is sleeping" / "Could not sync", or when the board's House Stuff, Earl Unplugged, sketchpad, or weather data needs manual updates.
---

# Earl Display Control

Everything required to bring the living-room TV display (VisuoSpatial Sketchpad) back online and refresh its content.

## Quick Response Checklist

1. **Wake requests ("Earl wake up", "Could not sync")**
   - Start the local server: `python -m http.server 8000` from `VisuoSpatialSketchpad/`.
   - Relaunch the kiosk: `Start-Process msedge.exe '--kiosk http://localhost:8000/sketchpad.html --edge-kiosk-type=fullscreen'`.
   - Watch the exec log for a steady stream of `GET /earl_mind.json ... 200` lines to confirm it is healthy.
2. **Content tweaks (House Stuff, Earl Unplugged, sketchpad, weather)**
   - Prefer the `EarlMind` helper methods in `earl_api.py`.
   - If you edit JSON directly, remember to bump `meta.last_updated` and `meta.update_count`.
   - Relaunch the kiosk so changes render immediately.

## Waking the Display (Server + Kiosk)

### 1. Restart the local server
- Run inside `C:\Users\Stuart\.openclaw\workspace\VisuoSpatialSketchpad`:
  ```powershell
  python -m http.server 8000
  ```
- Let OpenClaw background the process so the shell prompt returns.
- If another python server is stuck, kill it (`taskkill /IM python.exe /F`) or terminate the specific exec session before relaunching.
- Repeated reminders such as "Earl is sleeping" or "Could not sync" mean this step is required.

### 2. Relaunch the Edge kiosk (full-screen TV browser)
- From any directory:
  ```powershell
  Start-Process msedge.exe '--kiosk http://localhost:8000/sketchpad.html --edge-kiosk-type=fullscreen'
  ```
- Always rerun after a wake cycle. Edge may appear open yet still cache the old page; forcing a kiosk relaunch guarantees the new JSON is loaded.

### 3. Recognizing sleep states
- The HTML fallback says "Earl is sleeping, text to wake him up." Treat any wake ping as instructions to perform the two steps above.
- Exec logs that end with `GET /earl_mind.json ... 200` followed by a process exit (code 1) mean the http.server died on its own; restart both components.

## Editing Earl's Mind (earl_mind.json)
All tiles, notes, and takes originate from `VisuoSpatialSketchpad/earl_mind.json`. Use the helper whenever possible:

```python
from earl_api import EarlMind
mind = EarlMind()
```

### House Stuff (Important board)
```python
mind.post_house_stuff(
    title="Phil is down bad",
    detail="He is sick. Be kind, bring water, keep the noise down.",
    priority="high",
    category="care",
    icon=":sick-face:")
```
- Remove items with `mind.resolve_house_stuff(item_id)` or clear all with `mind.clear_house_stuff()`.

### Earl Unplugged (takes)
```python
mind.hot_take(
    topic="Earl has a wife",
    take="Earl has a wife!!!",
    heat=0.73,
    emoji=":ring:")
```
- Calling `hot_take` again with the same topic updates it; use `mind.drop_take(topic)` to delete.
- For manual reordering, edit `data['earl_unplugged']` or run helper scripts such as `reorder_take.py`, then rewrite the JSON with `ensure_ascii=False, indent=2` and bump `meta`.

### Sketchpad doodles and notes
```python
mind.doodle('[guitar]', x=0.75, y=0.48, size=32, color='#facc15', note='Riff time')
mind.sketch_note('Milk pitchers left out', x=0.62, y=0.22, size=12, color='#9ab0c4')
```
- Positions are normalized (0-1) and render immediately after you relaunch the kiosk.
- Only run `mind.clear_sketchpad()` when explicitly told to wipe the board.

### Mood, weather, and vibe refresh
Use the ready-made script to pull Open-Meteo data, update mood/energy, drop a weather doodle, and log a pattern.
```powershell
python update_weather_ping.py
```

### Manual JSON edits
If speed matters and you edit the JSON directly:
1. Load the file, mutate objects, and `json.dump(..., ensure_ascii=False, indent=2)` when writing back.
2. Immediately refresh the footer metadata:
   ```python
   from datetime import datetime, timezone
   data['meta']['last_updated'] = datetime.now(timezone.utc).isoformat()
   data['meta']['update_count'] = data['meta'].get('update_count', 0) + 1
   ```
3. Relaunch the kiosk to display the new state.

## Troubleshooting
- **Server keeps dying within minutes**
  - Check for multiple python processes (`Get-Process python`) and stop duplicates.
  - Ensure you started the server from the VisuoSpatialSketchpad directory so `earl_mind.json` and `sketchpad.html` resolve.
- **Edge refuses kiosk mode**
  - Kill stray windows: `taskkill /IM msedge.exe /F`, then rerun the kiosk command.
- **Content not updating**
  - Reopen the JSON to confirm your change saved.
  - Relaunch the kiosk to bust any cache.
  - Remember that `update_weather_ping.py` overwrites mood/energy/sketchpad weather markers, so run it whenever someone requests a fresh weather ping.

Tight loop: restart server -> relaunch kiosk -> apply content change -> relaunch kiosk (if needed). Follow it every time the house texts "wake up" so Earl always responds immediately.
