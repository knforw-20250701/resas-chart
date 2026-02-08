import subprocess
import os

# Order: Oldest to Newest
commits = [
    ("50f14f8", "人口比較実装"),
    ("700fd7b", ".envをgitignoreに追加"),
    ("41f4348", "APIキーの秘匿化"),
    ("bf54d7f", "Nodeバージョンを更新"),
    ("25459af", "GitHub Actionsをv4に更新"),
    ("d8b50fa", "コントリビューターを更新"),
    ("56e2d95", "README加筆修正")
]

def run(cmd):
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd, capture_output=True, text=True)

def main():
    # 1. Back to main
    run(['git', 'checkout', 'main'])
    
    # 2. Create target branch
    run(['git', 'branch', '-D', 'target-main']) # Cleanup old attempt
    run(['git', 'checkout', '--orphan', 'target-main'])
    run(['git', 'reset', '--hard'])
    
    # 3. Step by step checkout and commit
    # Note: Using hashes that we know are in the refs/original or origin/main
    # Actually, let's use origin/main's commits.
    # Current origin/main has 7 commits. Let's get them.
    res = run(['git', 'rev-list', '--reverse', 'origin/main'])
    h_list = res.stdout.strip().splitlines()
    
    if len(h_list) != 7:
        print(f"Warning: Expected 7 commits from origin/main, found {len(h_list)}")
    
    for i, h in enumerate(h_list):
        msg = commits[i][1] if i < len(commits) else f"Commit {i}"
        
        # Checkout EVERYTHING from that commit into current worktree
        run(['git', 'checkout', h, '--', '.'])
        
        # Add all (including deletions)
        run(['git', 'add', '-A'])
        
        # Commit
        run(['git', 'commit', '--allow-empty', '-m', msg])
        print(f"Committed {h} as: {msg}")

    print("Reconstruction finished on branch 'target-main'")

if __name__ == "__main__":
    main()
