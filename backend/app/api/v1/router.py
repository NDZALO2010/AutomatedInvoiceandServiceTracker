from fastapi import APIRouter

from app.api.v1 import admin, auth, clients, invoices, services, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
api_router.include_router(invoices.router, prefix="/invoices", tags=["invoices"])
