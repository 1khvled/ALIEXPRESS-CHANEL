"""AWS deployment assets (CloudFormation + Lambda container).

This package exists so ``infra.aws.lambda_handler`` can be imported by tests
and linters.  Nothing here is imported by the Vercel app or the GitHub cron.
"""
