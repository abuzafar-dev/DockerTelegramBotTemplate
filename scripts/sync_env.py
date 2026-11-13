import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATED = {
    'SECRET_KEY': lambda: secrets.token_urlsafe(50),
    'API_TOKEN': lambda: secrets.token_urlsafe(32),
}


def parse(text):
    return {line.split('=', 1)[0] for line in text.splitlines() if '=' in line and not line.startswith('#')}


def main():
    env_path = ROOT / '.env'
    example = (ROOT / '.env.example').read_text()
    current = env_path.read_text() if env_path.exists() else ''
    existing = parse(current)
    added = []
    for line in example.splitlines():
        if '=' not in line or line.startswith('#'):
            continue
        key, value = line.split('=', 1)
        if key in existing:
            continue
        if key in GENERATED:
            value = GENERATED[key]()
        added.append(f'{key}={value}')
    if added:
        if current and not current.endswith('\n'):
            current += '\n'
        env_path.write_text(current + '\n'.join(added) + '\n')
        print('==> .env ga qo\'shildi: ' + ', '.join(item.split('=', 1)[0] for item in added))


if __name__ == '__main__':
    main()
