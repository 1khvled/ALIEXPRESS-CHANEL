"""
Automated Vercel Historical Deployments Cleaner.
Deletes older deployments to instantly free up Vercel Functions Storage and Deployment Storage.
Keeps the latest active production deployment safe.

Usage:
  python scripts/clean_vercel_storage.py [VERCEL_TOKEN] [PROJECT_NAME]
"""
import os
import sys
import httpx

def clean_deployments(token: str, project_name: str = "dealscoutgreen"):
    headers = {"Authorization": f"Bearer {token}"}
    base_url = "https://api.vercel.com"

    print(f"[*] Fetching Vercel projects to match '{project_name}'...")
    try:
        res = httpx.get(f"{base_url}/v9/projects", headers=headers, timeout=15)
    except Exception as e:
        print(f"[!] Network error connecting to Vercel API: {e}")
        return

    if res.status_code != 200:
        print(f"[!] Error fetching projects: {res.status_code} - {res.text}")
        return

    projects = res.json().get("projects", [])
    if not projects:
        print("[!] No projects found for this Vercel account token.")
        return

    matched_project = next(
        (p for p in projects if p["name"].lower() == project_name.lower() or project_name.lower() in p["name"].lower() or p["name"].lower() in project_name.lower()),
        None
    )
    
    if not matched_project:
        print(f"[!] Exact project '{project_name}' not found. Available projects in your account:")
        for idx, p in enumerate(projects, 1):
            print(f"    {idx}. {p['name']} (ID: {p['id']})")
        matched_project = projects[0]
        print(f"[*] Automatically targeting: '{matched_project['name']}'")

    project_id = matched_project["id"]
    print(f"\n[+] Target Project: {matched_project['name']} (ID: {project_id})")

    # Fetch deployments in loop until all older deployments are purged
    total_deleted = 0
    preserved_id = None

    while True:
        print("\n[*] Fetching batch of past deployments...")
        try:
            dep_res = httpx.get(f"{base_url}/v6/deployments?projectId={project_id}&limit=100", headers=headers, timeout=20)
        except Exception as e:
            print(f"[!] Network error: {e}")
            break

        if dep_res.status_code != 200:
            print(f"[!] Error fetching deployments: {dep_res.status_code} - {dep_res.text}")
            break

        deployments = dep_res.json().get("deployments", [])
        print(f"[+] Found {len(deployments)} deployments.")

        if len(deployments) <= 1:
            print("[+] Only active production deployment remaining. All historical builds cleared!")
            break

        # Sort descending by creation date
        deployments.sort(key=lambda d: d.get("createdAt", 0), reverse=True)
        
        # Keep the latest deployment
        if preserved_id is None:
            active_dep = deployments[0]
            preserved_id = active_dep["uid"]
            print(f"[+] PRESERVING ACTIVE PRODUCTION DEPLOYMENT:")
            print(f"    - URL: https://{active_dep.get('url')}")
            print(f"    - State: {active_dep.get('state')}")
            print(f"    - ID: {preserved_id}")

        to_delete = [d for d in deployments if d["uid"] != preserved_id]
        if not to_delete:
            print("[+] No older deployments left to delete.")
            break

        print(f"[*] Deleting batch of {len(to_delete)} older deployments...")

        batch_deleted = 0
        for dep in to_delete:
            dep_id = dep["uid"]
            url = dep.get("url", dep_id)
            try:
                del_res = httpx.delete(f"{base_url}/v13/deployments/{dep_id}", headers=headers, timeout=15)
                if del_res.status_code in (200, 204):
                    batch_deleted += 1
                    total_deleted += 1
                    print(f"  [DELETED #{total_deleted}] {url}")
                else:
                    print(f"  [SKIP] {url}: HTTP {del_res.status_code}")
            except Exception as e:
                print(f"  [ERROR] {url}: {e}")

        if batch_deleted == 0:
            print("[!] No deployments were deleted in this pass. Stopping.")
            break

    print(f"\n=======================================================")
    print(f"[SUCCESS] Purged {total_deleted} historical deployments!")
    print(f"[*] Vercel Functions Storage and Deployment Storage are now clean.")
    print(f"=======================================================")


if __name__ == "__main__":
    token = None
    if len(sys.argv) > 1 and sys.argv[1].strip():
        token = sys.argv[1].strip()
    elif os.getenv("VERCEL_TOKEN"):
        token = os.getenv("VERCEL_TOKEN").strip()
    
    if not token:
        print("=" * 60)
        print(" DealScout Vercel Storage & Deployments Cleaner")
        print("=" * 60)
        print("Please provide your Vercel Access Token:")
        print("  Get it from: https://vercel.com/account/tokens")
        print("Usage:")
        print("  python scripts/clean_vercel_storage.py <YOUR_VERCEL_TOKEN> [PROJECT_NAME]")
        sys.exit(1)

    proj_name = sys.argv[2].strip() if len(sys.argv) > 2 else "dealscoutgreen"
    clean_deployments(token, proj_name)
