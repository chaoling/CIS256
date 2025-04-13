import os
import subprocess
import shutil
from pathlib import Path
import uuid
import argparse

DEFAULT_BRANCH = "main"
TEMP_BASE = "/tmp"

def find_nested_git_dirs(root_path):
    nested_git_dirs = []
    root_path = Path(root_path).resolve()
    top_git_path = root_path / ".git"

    for dirpath, dirnames, filenames in os.walk(root_path):
        if Path(dirpath).resolve() == root_path and ".git" in dirnames:
            dirnames.remove(".git")
        if ".git" in dirnames:
            repo_path = Path(dirpath).resolve()
            if (repo_path / ".git") != top_git_path:
                nested_git_dirs.append(repo_path)
            dirnames[:] = []
    return nested_git_dirs

def run(cmd, cwd=None, dry_run=False):
    if dry_run:
        print(f"📝 [dry-run] Would run: {cmd}")
    else:
        print(f"📦 Running: {cmd}")
        result = subprocess.run(cmd, cwd=cwd, shell=True, text=True)
        if result.returncode != 0:
            print(f"❌ Command failed: {cmd}")
            exit(1)

def remote_exists(remote_name, cwd="."):
    result = subprocess.run(
        f"git remote get-url {remote_name}",
        cwd=cwd,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def has_uncommitted_changes(cwd="."):
    result = subprocess.run(
        "git status --porcelain",
        cwd=cwd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return bool(result.stdout.strip())

def has_valid_head(repo_path):
    head_file = Path(repo_path) / ".git" / "HEAD"
    return head_file.exists() and head_file.read_text().strip().startswith("ref:")

def has_commits(repo_path):
    result = subprocess.run(
        "git rev-parse HEAD",
        cwd=repo_path,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def get_default_branch(repo_path):
    head_file = Path(repo_path) / ".git" / "HEAD"
    if head_file.exists():
        line = head_file.read_text().strip()
        if line.startswith("ref:"):
            return line.split("/")[-1]  # last part of ref
    return None

def main():
    parser = argparse.ArgumentParser(description="Import nested Git repos as subtrees.")
    parser.add_argument("--squash", action="store_true", help="Squash history into a single commit")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done, without making changes")
    parser.add_argument("--fallback-branch", default=DEFAULT_BRANCH, help="Branch to use if detection fails (default: main)")
    args = parser.parse_args()

    squash = args.squash
    dry_run = args.dry_run
    fallback_branch = args.fallback_branch
    root = Path(".").resolve()

    if not (root / ".git").exists():
        if dry_run:
            print("🌀 [dry-run] Would initialize new Git repo")
            print("📝 [dry-run] Would make initial empty commit")
        else:
            print("🌀 Initializing new Git repo...")
            run("git init", cwd=root)
            run('git commit --allow-empty -m "Initial commit"', cwd=root)

    git_repos = find_nested_git_dirs(root)
    if not git_repos:
        print("✅ No nested .git repos found.")
        return

    print(f"🔍 Found {len(git_repos)} nested Git repos:")

    for repo_path in git_repos:
        rel_path = repo_path.relative_to(root)
        safe_name = "_".join(rel_path.parts) or f"repo_{uuid.uuid4().hex[:6]}"
        remote_name = safe_name.replace("-", "_")
        temp_path = Path(TEMP_BASE) / f"tmp_{remote_name}"

        print(f"\n➡️  Processing {rel_path}")

        if temp_path.exists() and not dry_run:
            shutil.rmtree(temp_path)

        if dry_run:
            print(f"📝 [dry-run] Would move {repo_path} to {temp_path}")
        else:
            shutil.move(repo_path, temp_path)

        # Validate repo
        if not dry_run and not has_valid_head(temp_path):
            print(f"❌ Skipping: {temp_path} has no valid HEAD.")
            continue

        if not dry_run and not has_commits(temp_path):
            print(f"⚠️ Skipping: {temp_path} has no commits.")
            continue

        # Detect branch
        detected_branch = get_default_branch(temp_path) or fallback_branch
        print(f"🔎 Using branch '{detected_branch}' for {remote_name}")

        prefix_path = root / rel_path
        if prefix_path.exists():
            if dry_run:
                print(f"📝 [dry-run] Would delete existing folder: {prefix_path}")
            else:
                print(f"⚠️  Deleting existing folder: {prefix_path}")
                shutil.rmtree(prefix_path)

        if not dry_run and (prefix_path / ".git").exists():
            print(f"🧹 Removing leftover .git from {prefix_path}")
            shutil.rmtree(prefix_path / ".git")

        if not dry_run:
            print("🔍 Checking for uncommitted changes...")
            if has_uncommitted_changes(cwd=root):
                run("git add -A", cwd=root)
                run('git commit -m "Prepare clean state for subtree import"', cwd=root)
            else:
                print("✅ Working tree is clean.")

        if remote_exists(remote_name, cwd=root):
            if dry_run:
                print(f"📝 [dry-run] Would remove existing remote: {remote_name}")
            else:
                print(f"⚠️  Removing existing remote: {remote_name}")
                run(f"git remote remove {remote_name}", cwd=root)

        run(f"git remote add {remote_name} {temp_path}", cwd=root, dry_run=dry_run)
        run(f"git fetch {remote_name}", cwd=root, dry_run=dry_run)

        prefix_arg = f"--prefix={rel_path}"
        squash_arg = "--squash" if squash else ""
        run(f"git subtree add {prefix_arg} {remote_name} {detected_branch} {squash_arg}", cwd=root, dry_run=dry_run)
        run(f"git remote remove {remote_name}", cwd=root, dry_run=dry_run)

        if not dry_run and temp_path.exists():
            print(f"🧹 Cleaning up {temp_path}")
            shutil.rmtree(temp_path)

        print(f"✅ {'[dry-run] Would import' if dry_run else 'Imported'} {rel_path}")

    print("\n🎉 Done! (dry-run mode ON)" if dry_run else "\n🎉 All nested repos imported successfully!")

if __name__ == "__main__":
    main()
