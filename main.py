"""
Vercel Serverless Entrypoint Proxy for DealScout DZ.
Exports the FastAPI application instance from api.index for Vercel deployment.
"""
from api.index import app

__all__ = ["app"]
