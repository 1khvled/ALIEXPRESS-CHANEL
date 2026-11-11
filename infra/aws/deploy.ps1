# DealScout AWS runtime deployment (Windows / PowerShell)
#
# Nothing is created until you pass -ConfirmDeploy. The first run only checks
# your session, builds the image and pushes it to ECR.
#
#   aws login --region eu-north-1 --profile agent-toolkit
#   .\infra\aws\deploy.ps1                       # dry run (build + push only)
#   .\infra\aws\deploy.ps1 -ConfirmDeploy        # create/update the stack
#
# All resources stay in eu-north-1 (the project's assigned Region).

[CmdletBinding()]
param(
    [string]$Profile = "agent-toolkit",
    [string]$Region = "eu-north-1",
    [string]$StackName = "dealscout-runtime",
    [string]$RepoName = "dealscout-runtime",
    [string]$ImageTag = "latest",
    [string]$ScheduleExpression = "rate(5 minutes)",
    [string]$SecretArn = "",
    [string]$AlarmEmail = "",
    [ValidateSet("off", "shadow", "enforce")]
    [string]$IntelligenceMode = "shadow",
    [switch]$SkipBuild,
    [switch]$ConfirmDeploy
)

$ErrorActionPreference = "Stop"

function Write-Step([string]$Message) {
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

# Make the standard AWS CLI location available when it is not on PATH.
if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
    $candidate = Join-Path $env:LOCALAPPDATA "Programs\Amazon\AWSCLIV2"
    if (Test-Path (Join-Path $candidate "aws.exe")) {
        $env:PATH = "$candidate;$env:PATH"
    } else {
        throw "AWS CLI not found. Install AWSCLIV2 or add aws.exe to PATH."
    }
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker is required to build the Lambda container image."
}

Write-Step "Verifying AWS session (profile=$Profile, region=$Region)"
$identityRaw = aws sts get-caller-identity --profile $Profile --output json 2>&1
if ($LASTEXITCODE -ne 0) {
    throw "AWS session is not valid. Run: aws login --region $Region --profile $Profile`n$identityRaw"
}
$identity = $identityRaw | ConvertFrom-Json
$account = $identity.Account
Write-Host "Account: $account  ARN: $($identity.Arn)"

Write-Step "Checking account plan"
try {
    $planRaw = aws freetier get-account-plan-state --region $Region --profile $Profile --output json 2>$null
    if ($LASTEXITCODE -eq 0 -and $planRaw) {
        $plan = $planRaw | ConvertFrom-Json
        Write-Host "Plan: $($plan.accountPlanType)"
        if ($plan.accountPlanType -eq "FREE") {
            Write-Warning "FREE plan: confirm Lambda, S3, EventBridge Scheduler and CloudWatch are supported before deploying."
        }
    }
} catch {
    Write-Warning "Could not read the account plan (older CLI?). Continuing."
}

$registry = "$account.dkr.ecr.$Region.amazonaws.com"
$imageUri = "$registry/$RepoName`:$ImageTag"

Write-Step "Ensuring ECR repository '$RepoName' exists"
$describe = aws ecr describe-repositories --repository-names $RepoName --region $Region --profile $Profile --output json 2>$null
if ($LASTEXITCODE -ne 0) {
    aws ecr create-repository `
        --repository-name $RepoName `
        --region $Region `
        --profile $Profile `
        --image-scanning-configuration scanOnPush=true `
        --image-tag-mutability MUTABLE | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Could not create ECR repository." }
    Write-Host "Created repository."
} else {
    Write-Host "Repository already exists."
}

if (-not $SkipBuild) {
    Write-Step "Logging in to ECR"
    $password = aws ecr get-login-password --region $Region --profile $Profile
    if ($LASTEXITCODE -ne 0) { throw "Could not get ECR login password." }
    $password | docker login --username AWS --password-stdin $registry
    if ($LASTEXITCODE -ne 0) { throw "docker login failed." }

    Write-Step "Building image $imageUri"
    docker build -f infra/aws/Dockerfile -t $imageUri .
    if ($LASTEXITCODE -ne 0) { throw "docker build failed." }

    Write-Step "Pushing image"
    docker push $imageUri
    if ($LASTEXITCODE -ne 0) { throw "docker push failed." }
}

if (-not $ConfirmDeploy) {
    Write-Host ""
    Write-Host "Dry run complete. Image: $imageUri" -ForegroundColor Yellow
    Write-Host "Re-run with -ConfirmDeploy to create/update the CloudFormation stack." -ForegroundColor Yellow
    exit 0
}

Write-Step "Deploying CloudFormation stack '$StackName'"
$overrides = @(
    "ImageUri=$imageUri",
    "ScheduleExpression=$ScheduleExpression",
    "TelegramSecretArn=$SecretArn",
    "IntelligenceMode=$IntelligenceMode",
    "AlarmEmail=$AlarmEmail"
)

aws cloudformation deploy `
    --template-file infra/aws/template.yaml `
    --stack-name $StackName `
    --capabilities CAPABILITY_IAM `
    --parameter-overrides @overrides `
    --region $Region `
    --profile $Profile `
    --no-fail-on-empty-changeset
if ($LASTEXITCODE -ne 0) { throw "CloudFormation deploy failed." }

Write-Step "Stack outputs"
aws cloudformation describe-stacks `
    --stack-name $StackName `
    --region $Region `
    --profile $Profile `
    --query "Stacks[0].Outputs" `
    --output table

Write-Host ""
Write-Host "Deployed. Next steps:" -ForegroundColor Green
Write-Host "  1. Store bot secrets in Secrets Manager and pass -SecretArn on the next deploy."
Write-Host "  2. Watch CloudWatch logs for at least one full run."
Write-Host "  3. Disable the GitHub cron schedule (set repo variable DEALSCOUT_RUNTIME=aws) only after AWS is healthy."
Write-Host "  4. Check your spend limit in AWS Settings > Billing."
