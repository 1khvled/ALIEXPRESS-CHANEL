# DealScout AWS runtime (Phase 2)

**Status: built, not deployed.** Nothing in this folder has been applied to an
AWS account. Deployment is an explicit, manual action and requires a valid
`aws login` session plus your approval.

This runtime runs the **same** `scripts/post_recent_deals.py` and
`scripts/post_france_deals.py` that GitHub Actions runs. No business logic is
duplicated, so a deal that works locally works identically on Lambda.

```
EventBridge Scheduler (rate 5 min, eu-north-1)
        |
        v
Lambda container image  (repo + requirements, 1024 MB, 15 min max)
        |
        +--> S3 bucket (private, versioned, encrypted)
        |       state/  -> storage/state/*.json   (dedup memory + intelligence model)
        |       db/     -> deals.db               (audit database)
        |
        +--> Telegram Bot API -> @DzAliexpress0 / @francedealsdz
```

## Why this exists

| GitHub Actions cron | AWS runtime |
|---|---|
| Best-effort scheduling; runs queue and slip | EventBridge fires on time |
| Ephemeral runner, state committed to git (~288 commits/day) | State in S3, no git churn |
| 6-hour job limit, shared runners | 15-minute Lambda, reserved concurrency 1 |
| No infrastructure alarms | CloudWatch alarms -> SNS email |

GitHub remains the **control plane** (code, review, Phase-3 controller).
AWS becomes the **data plane** (reliable execution).

## Prerequisites

- AWS CLI with a valid session: `aws login --region eu-north-1 --profile agent-toolkit`
- Docker Desktop (to build the container image)
- The project's assigned Region is **eu-north-1**; every resource is regional
  and created there. No Lambda@Edge, no StackSets, no cross-Region replication.
- Confirm your spend limit in **AWS Settings > Billing** before deploying.
  A 5-minute schedule is ~8,640 invocations/month; see cost below.

## 1. Store the bot secrets (recommended)

Create one Secrets Manager secret whose value is a JSON object. The handler
copies every key into the process environment before importing the app.

```bash
aws secretsmanager create-secret \
  --name dealscout/runtime \
  --region eu-north-1 \
  --profile agent-toolkit \
  --secret-string '{
    "TELEGRAM_BOT_TOKEN": "123:ABC",
    "TARGET_CHANNEL_ID": "@DzAliexpress0",
    "ADMIN_USER_ID": "5625295907",
    "ALIEXPRESS_AFFILIATE_APP_KEY": "...",
    "ALIEXPRESS_AFFILIATE_APP_SECRET": "...",
    "FACEBOOK_PAGE_ACCESS_TOKEN": "...",
    "FACEBOOK_PAGE_ID": "1451244491398196",
    "FACEBOOK_AUTO_POST_ENABLED": "true",
    "DUPLICATE_COOLDOWN_HOURS": "4",
    "INTELLIGENCE_MODE": "shadow"
  }'
```

Use the returned ARN as `-SecretArn` / `SECRET_ARN`. Prefer Secrets Manager over
plain Lambda environment variables for anything sensitive.

## 2. Deploy

Windows:

```powershell
# Dry run: verifies session, creates the ECR repo, builds and pushes the image.
.\infra\aws\deploy.ps1

# Create/update the stack.
.\infra\aws\deploy.ps1 -ConfirmDeploy -SecretArn "arn:aws:secretsmanager:eu-north-1:...:secret:dealscout/runtime" -AlarmEmail "you@example.com"
```

Linux / CI:

```bash
./infra/aws/deploy.sh                 # dry run
SECRET_ARN="arn:..." ALARM_EMAIL="you@example.com" ./infra/aws/deploy.sh --confirm
```

From GitHub: **Actions -> Deploy AWS Runtime -> Run workflow**, type `DEPLOY`.
This uses OIDC; set repository variable `AWS_DEPLOY_ROLE_ARN` first.

The stack creates:

- private, versioned, encrypted S3 bucket
- Lambda container function (reserved concurrency 1)
- EventBridge Scheduler schedule
- CloudWatch log group (14-day retention)
- error + throttle alarms and an SNS topic

## 3. Verify before cutting over

1. CloudWatch -> Log group `/aws/lambda/dealscout-runtime-runtime` -> one full
   run should show `[LAMBDA] completed ...`.
2. S3 -> `state/` contains `published_state.json` and
   `intelligence_model.json`; `db/deals.db` exists.
3. The channel receives a post, and `published_state.json` grows.
4. Check **no duplicate** post: wait two runs and compare channel history.
5. Only then set repository variable `DEALSCOUT_RUNTIME=aws`. The GitHub cron
   job skips automatically (manual dispatch still works).
6. Keep `bot_cron.yml` in the repo as the rollback path.

## Rollback

1. Delete repository variable `DEALSCOUT_RUNTIME` (GitHub cron resumes on the
   next 5-minute tick).
2. Optionally delete the stack:

```bash
aws cloudformation delete-stack \
  --stack-name dealscout-runtime \
  --region eu-north-1 \
  --profile agent-toolkit
```

The S3 bucket is retained by CloudFormation? **No** — this template has no
`DeletionPolicy: Retain`. Export or copy `state/` before deleting the stack if
you want to keep the learning history. (Deliberate: a stale state bucket is
worse than a clean start.)

## Cost (eu-north-1, approximate)

| Item | Assumption | Monthly |
|---|---|---|
| Lambda | 1024 MB, 90 s per run, 8,640 runs | ~$8 |
| Lambda requests | 8,640 | ~$0.00 |
| EventBridge Scheduler | 8,640 invocations | ~$0.01 |
| S3 + requests | < 100 MB, versioned | < $1 |
| CloudWatch logs | 14-day retention | ~$1 |
| **Total** | | **~$10 / month** |

If a run takes 4 minutes the Lambda line is ~$21/month. Measure the real
duration in CloudWatch, then tune `MemorySize` and `TimeoutSeconds`.
Graviton (`arm64`) is ~20% cheaper but requires an arm64 build host.

## Safety interlocks

- **State download is fail-closed.** If S3 sync fails, the handler aborts
  before publishing rather than publishing without dedup memory.
- **Reserved concurrency 1.** A run that overruns the schedule throttles the
  next one (alarm fires) instead of posting duplicates in parallel.
- **Intelligence defaults to `shadow`.** The deterministic scorer logs only
  until you explicitly deploy `-IntelligenceMode enforce`.
- **No `LIVE` toggle at deploy time.** The schedule is enabled by the stack;
  the in-process night pause (00:00–08:00 Algiers) still applies.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `state download failed; refusing to publish` | S3 permissions or wrong bucket; check the execution role |
| `Task timed out` | Raise `TimeoutSeconds` (max 900) or `MemorySize` |
| `Throttles` alarm | Previous run still active; lengthen the schedule |
| No posts, no errors | Check `is_deal_posting_due` and the Algiers night pause |
| `ModuleNotFoundError` | A new dependency was added to `requirements.txt`; rebuild the image |

## Files

| File | Purpose |
|---|---|
| `template.yaml` | CloudFormation stack (S3, IAM, Lambda, Scheduler, alarms) |
| `Dockerfile` | Lambda container image |
| `lambda_handler.py` | Sync state -> run publishers -> sync state |
| `state_sync.py` | S3 download/upload helpers (unit-testable, boto3 lazy) |
| `deploy.ps1` / `deploy.sh` | Build, push, deploy (dry-run by default) |
