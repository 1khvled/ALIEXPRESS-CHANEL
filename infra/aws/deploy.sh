#!/usr/bin/env bash
# DealScout AWS runtime deployment (Linux / macOS / GitHub Actions).
#
# Nothing is created until --confirm is passed. First run only builds/pushes.
#
#   aws login --region eu-north-1 --profile agent-toolkit
#   ./infra/aws/deploy.sh                # dry run
#   ./infra/aws/deploy.sh --confirm      # create/update the stack
#
# All resources stay in eu-north-1 (the project's assigned Region).

set -euo pipefail

PROFILE="${AWS_PROFILE:-agent-toolkit}"
REGION="${AWS_REGION:-eu-north-1}"
STACK_NAME="${STACK_NAME:-dealscout-runtime}"
REPO_NAME="${REPO_NAME:-dealscout-runtime}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
SCHEDULE_EXPRESSION="${SCHEDULE_EXPRESSION:-rate(5 minutes)}"
SECRET_ARN="${SECRET_ARN:-}"
ALARM_EMAIL="${ALARM_EMAIL:-}"
INTELLIGENCE_MODE="${INTELLIGENCE_MODE:-shadow}"
CONFIRM=0
SKIP_BUILD=0

for arg in "$@"; do
  case "$arg" in
    --confirm) CONFIRM=1 ;;
    --skip-build) SKIP_BUILD=1 ;;
    *) echo "Unknown argument: $arg" >&2; exit 2 ;;
  esac
done

step() { printf '\n==> %s\n' "$1"; }

step "Verifying AWS session (profile=$PROFILE, region=$REGION)"
if ! IDENTITY_JSON="$(aws sts get-caller-identity --profile "$PROFILE" --output json 2>&1)"; then
  echo "$IDENTITY_JSON" >&2
  echo "AWS session is not valid. Run: aws login --region $REGION --profile $PROFILE" >&2
  exit 1
fi
ACCOUNT="$(printf '%s' "$IDENTITY_JSON" | python -c 'import json,sys; print(json.load(sys.stdin)["Account"])')"
echo "Account: $ACCOUNT"

step "Checking account plan"
if aws freetier get-account-plan-state --region "$REGION" --profile "$PROFILE" --output json >/tmp/dealscout-plan.json 2>/dev/null; then
  PLAN="$(python -c 'import json; print(json.load(open("/tmp/dealscout-plan.json")).get("accountPlanType","UNKNOWN"))')"
  echo "Plan: $PLAN"
  if [ "$PLAN" = "FREE" ]; then
    echo "WARNING: FREE plan — confirm Lambda/S3/Scheduler/CloudWatch support before deploying." >&2
  fi
else
  echo "Could not read the account plan (older CLI?). Continuing."
fi

REGISTRY="$ACCOUNT.dkr.ecr.$REGION.amazonaws.com"
IMAGE_URI="$REGISTRY/$REPO_NAME:$IMAGE_TAG"

step "Ensuring ECR repository '$REPO_NAME' exists"
if ! aws ecr describe-repositories --repository-names "$REPO_NAME" --region "$REGION" --profile "$PROFILE" >/dev/null 2>&1; then
  aws ecr create-repository \
    --repository-name "$REPO_NAME" \
    --region "$REGION" \
    --profile "$PROFILE" \
    --image-scanning-configuration scanOnPush=true \
    --image-tag-mutability MUTABLE >/dev/null
  echo "Created repository."
else
  echo "Repository already exists."
fi

if [ "$SKIP_BUILD" -eq 0 ]; then
  step "Logging in to ECR"
  aws ecr get-login-password --region "$REGION" --profile "$PROFILE" \
    | docker login --username AWS --password-stdin "$REGISTRY"

  step "Building image $IMAGE_URI"
  docker build -f infra/aws/Dockerfile -t "$IMAGE_URI" .

  step "Pushing image"
  docker push "$IMAGE_URI"
fi

if [ "$CONFIRM" -ne 1 ]; then
  echo
  echo "Dry run complete. Image: $IMAGE_URI"
  echo "Re-run with --confirm to create/update the CloudFormation stack."
  exit 0
fi

step "Deploying CloudFormation stack '$STACK_NAME'"
aws cloudformation deploy \
  --template-file infra/aws/template.yaml \
  --stack-name "$STACK_NAME" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
      "ImageUri=$IMAGE_URI" \
      "ScheduleExpression=$SCHEDULE_EXPRESSION" \
      "TelegramSecretArn=$SECRET_ARN" \
      "IntelligenceMode=$INTELLIGENCE_MODE" \
      "AlarmEmail=$ALARM_EMAIL" \
  --region "$REGION" \
  --profile "$PROFILE" \
  --no-fail-on-empty-changeset

step "Stack outputs"
aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --profile "$PROFILE" \
  --query 'Stacks[0].Outputs' \
  --output table

cat <<'EOF'

Deployed. Next steps:
  1. Store bot secrets in Secrets Manager and pass SECRET_ARN on the next deploy.
  2. Watch CloudWatch logs for at least one full run.
  3. Set GitHub repo variable DEALSCOUT_RUNTIME=aws only after AWS is healthy.
  4. Check your spend limit in AWS Settings > Billing.
EOF
