import json
from pathlib import Path
path = Path('earl_mind.json')
mind = json.loads(path.read_text(encoding='utf-8'))
mind['earl_unplugged'] = [t for t in mind['earl_unplugged'] if t['topic'] != 'Late-night noise levels']
path.write_text(json.dumps(mind, indent=2, ensure_ascii=False), encoding='utf-8')
