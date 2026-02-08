import subprocess
import sys

messages = [
    "人口比較実装",
    ".envをgitignoreに追加",
    "APIキーの秘匿化",
    "Nodeバージョンを更新",
    "GitHub Actionsをv4に更新",
    "コントリビューターを更新",
    "README加筆修正"
]

def run(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result

def main():
    # 1. Get hashes from chronological order (oldest first)
    # We assume 'main' is the corrupted branch
    res = run(['git', 'rev-list', '--reverse', 'main'])
    h_list = res.stdout.strip().splitlines()
    
    if not h_list:
        print("No commits found.")
        return

    # 2. Create a new orphan branch
    run(['git', 'checkout', '--orphan', 'reconstructed-main'])
    run(['git', 'reset', '--hard'])
    
    # 3. Cherry-pick and commit with new message
    for i, h in enumerate(h_list):
        # We use -n (no-commit) to apply changes but allow us to set the message
        # We also need to handle empty commits specifically since cherry-pick -n 
        # doesn't like empty commits without extra flags usually.
        # However, for repo reconstruction, we can just use cherry-pick and then amend.
        
        # Actually, cherry-pick is better.
        run(['git', 'cherry-pick', h])
        
        # Now amend the message
        msg = messages[i] if i < len(messages) else f"Additional commit {i}"
        run(['git', 'commit', '--amend', '-m', msg])

    # 4. Final verification and branch swap
    print("Reconstruction complete. Check the log and then run:")
    print("git branch -M reconstructed-main main")

if __name__ == "__main__":
    main()
