# Earl Display Control Skill

This repo bundles everything needed to keep the VisuoSpatial Sketchpad (Earl's TV dashboard) awake and refreshed, plus the packaged `.skill` file you can upload to Clawhub or distribute however you like.

## Repo Layout

| Path | Purpose |
| --- | --- |
| `skills/earl-display-control/` | The actual Skill definition (SKILL.md). This is what Codex loads to learn the workflow. |
| `VisuoSpatialSketchpad/` | The supporting python + HTML bundle (`earl_api.py`, `update_weather_ping.py`, kiosk assets, etc.). |
| `VisuoSpatialSketchpad/earl_mind.template.json` | Sanitized starter state; copy it to `earl_mind.json` locally before running the board. |
| `dist/earl-display-control.skill` | Ready-to-share packaged Skill archive generated earlier. |

> Privacy note: the real `VisuoSpatialSketchpad/earl_mind.json` stays local and is gitignored by default. Rename the template or copy it over when you need a clean slate, but don't push the live house state to GitHub.

## Local Prep

1. (Optional) Create a clean virtual environment if you plan to hack on the helper scripts.
2. Update any content inside `skills/earl-display-control` or `VisuoSpatialSketchpad` as needed.
3. Re-run the weather or kiosk helper scripts locally to verify everything still works.

## Re-packaging

If you change anything and want a fresh `.skill` bundle:

```powershell
# from the workspace root
python "$env:APPDATA\npm\node_modules\openclaw\skills\skill-creator\scripts\package_skill.py" skills\earl-display-control dist
```

The script validates the skill and drops an updated `dist/earl-display-control.skill` file.

## Publishing to GitHub

1. `cd earl-display-control-repo`
2. `git init`
3. Review `.gitignore` (especially if you plan to exclude `earl_mind.json`).
4. `git add .`
5. `git commit -m "Initial import"`
6. `git remote add origin <your-repo-url>`
7. `git push -u origin main`

## Publishing to Clawhub

1. Log into https://clawhub.com with your GitHub account.
2. Create a new Skill entry and point it at the repo you just pushed **or** upload `dist/earl-display-control.skill` directly.
3. Fill in the metadata + thumbnail.
4. Publish. Clawhub will handle distribution.

Ping me if you need a sanitized `earl_mind.json` template or want to break the Skill into smaller modules.
