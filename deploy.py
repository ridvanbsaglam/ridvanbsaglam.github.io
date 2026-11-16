import subprocess
import os
import sys
from datetime import datetime

REPO_URL = "https://github.com/ridvanbsaglam/ridvanbsaglam.github.io.git"
REPO_DIR = os.path.dirname(os.path.abspath(__file__))

def run_cmd(cmd, check=True):
    print(f">> Running: {cmd}")
    res = subprocess.run(cmd, cwd=REPO_DIR, shell=True, text=True, capture_output=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr:
        print(res.stderr.strip(), file=sys.stderr)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed with code {res.returncode}: {cmd}")
    return res

def main():
    print("=" * 60)
    print("🚀 RIDVAN SAGLAM PORTFOLIO DEPLOYMENT ENGINE (.github.io)")
    print("=" * 60)

    # 1. Initialize git if not present
    if not os.path.exists(os.path.join(REPO_DIR, ".git")):
        print("Initialising local Git repository...")
        run_cmd("git init -b main")
    
    # 2. Configure user identity if not set locally
    run_cmd('git config user.name "Rıdvan Sağlam"', check=False)
    run_cmd('git config user.email "ridvanbsaglam@gmail.com"', check=False)

    # 3. Setup Remote Origin
    remotes = run_cmd("git remote -v", check=False).stdout
    if "origin" not in remotes:
        print(f"Setting remote origin to {REPO_URL}...")
        run_cmd(f"git remote add origin {REPO_URL}")
    else:
        run_cmd(f"git remote set-url origin {REPO_URL}")

    # 4. Stage and Commit
    print("Staging all portfolio files & interactive simulations...")
    run_cmd("git add -A")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Deploy portfolio & simulations update [{timestamp}]"
    
    status = run_cmd("git status --porcelain", check=False).stdout
    if status.strip():
        run_cmd(f'git commit -m "{commit_msg}"')
    else:
        print("No changes to commit. Working tree clean.")

    # 5. Push to GitHub Pages
    print("\nPushing to GitHub Pages (main branch)...")
    push_res = run_cmd("git push -u origin main", check=False)
    if push_res.returncode == 0:
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Portfolio deployed to GitHub Pages.")
        print("🌐 Live URL: https://ridvanbsaglam.github.io")
        print("=" * 60)
    else:
        print("\n" + "!" * 60)
        print("⚠️ Push failed or GitHub authentication required.")
        print("1) Ensure you created the repository 'ridvanbsaglam.github.io' at:")
        print("   https://github.com/new")
        print("2) If a browser login pops up, authenticate with your GitHub account.")
        print("3) Run 'python deploy.py' again.")
        print("!" * 60)

if __name__ == "__main__":
    main()
