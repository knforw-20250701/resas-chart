import sys

# Mapping with exact keys
mapping = {
    "docs: update README formatting": "README加筆修正",
    "Update contributors": "コントリビューターを更新",
    "chore: update GH Actions to v4": "GitHub Actionsをv4に更新",
    "fix: upgrade node version to 20 for build support": "Nodeバージョンを更新",
    "chore: inject VITE_ESTAT_API_KEY in deployment workflow": "APIキーの秘匿化",
    "chore: ignore .env and remove it from tracking": ".envをgitignoreに追加",
}

def main():
    # Read binary and decode as utf-8 (ignoring errors)
    try:
        raw_msg = sys.stdin.buffer.read()
        msg = raw_msg.decode('utf-8', errors='ignore').strip()
        
        if msg in mapping:
            # Output encoded utf-8
            sys.stdout.buffer.write(mapping[msg].encode('utf-8'))
            sys.stdout.buffer.write(b'\n')
        else:
            # Pass through original
            sys.stdout.buffer.write(raw_msg)
    except Exception as e:
        # Emergency fallback
        sys.exit(1)

if __name__ == "__main__":
    main()
