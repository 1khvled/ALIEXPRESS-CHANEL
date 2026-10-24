"""
Automated Vercel Historical Deployments Cleaner.
Deletes older deployments to instantly free up Vercel Functions Storage and Deployment Storage.
Keeps the latest active production deployment safe.

Usage:
  python scripts/clean_vercel_storage.py <VERCEL_TOKEN> [PROJECT_NAME]
"""
import sys
import httpx

def clean_deployments(token: str, project_name: str = "dealscout"):
    headers = {"Authorization": f"Bearer {token}"}
    base_url = "https://api.vercel.com"

    print(f"[*] Fetching projects to find '{project_name}'...")
    res = httpx.get(f"{base_url}/v9/projects", headers=headers, timeout=15)
    if res.status_code != 200:
        print(f"[!] Error fetching projects: {res.status_code} - {res.text}")
        return

    projects = res.json().get("projects", [])
    matched_project = next((p for p in projects if p["name"].lower() == project_name.lower() or project_name.lower() in p["name"].lower()), None)
    
    if not matched_project:
        print(f"[!] Project '{project_name}' not found. Available projects:")
        for p in projects:
            print(f"    - {p['name']} (ID: {p['id']})")
        if projects:
            matched_project = projects[0]
            print(f"[*] Defaulting to: {matched_project['name']}")
        else:
            return

    project_id = matched_project["id"]
    print(f"[+] Targeting project: {matched_project['name']} (ID: {project_id})")

    # Fetch deployments in loop until all older deployments are purged
    total_deleted = 0
    preserved_id = None

    while True:
        print("[*] Fetching past deployments...")
        dep_res = httpx.get(f"{base_url}/v6/deployments?projectId={project_id}&limit=100", headers=headers, timeout=20)
        if dep_res.status_code != 200:
            print(f"[!] Error fetching deployments: {dep_res.status_code} - {dep_res.text}")
            break

        deployments = dep_res.json().get("deployments", [])
        print(f"[+] Retrieved {len(deployments)} deployments.")

        if len(deployments) <= 1:
            print("[+] Only active deployment remaining. All historical builds cleared!")
            break

        # Sort descending by creation date
        deployments.sort(key=lambda d: d.get("createdAt", 0), reverse=True)
        
        # Keep the latest deployment
        if preserved_id is None:
            active_dep = deployments[0]
            preserved_id = active_dep["uid"]
            print(f"[+] Preserving active deployment: {active_dep.get('url')} (State: {active_dep.get('state')})")

        to_delete = [d for d in deployments if d["uid"] != preserved_id]
        if not to_delete:
            print("[+] No older deployments left to delete.")
            break

        print(f"[*] Deleting batch of {len(to_delete)} older deployments...")

        batch_deleted = 0
        for dep in to_delete:
            dep_id = dep["uid"]
            url = dep.get("url", dep_id)
            del_res = httpx.delete(f"{base_url}/v13/deployments/{dep_id}", headers=headers, timeout=15)
            if del_res.status_code in (200, 204):
                batch_deleted += 1
                total_deleted += 1
                print(f"  [OK] Deleted ({total_deleted}): {url}")
            else:
                print(f"  [SKIP] {url}: {del_res.status_code}")

        if batch_deleted == 0:
            print("[!] No deployments were deleted in this pass. Stopping.")
            break

    print(f"\n[DONE] Successfully deleted {total_deleted} historical deployments!")
    print("[*] Vercel Functions Storage and Deployment Storage have been freed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/clean_vercel_storage.py <VERCEL_TOKEN> [PROJECT_NAME]")
        sys.exit(1)
    
    token_arg = sys.argv[1].strip()
    proj_arg = sys.argv[2].strip() if len(sys.argv) > 2 else "app"
    clean_deployments(token_arg, proj_arg)

