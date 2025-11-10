from fastapi import APIRouter

# Import domain routers
from .domains.patron.router import router as patron_router
from .domains.item.router import router as item_router  
from .domains.transaction.router import router as transaction_router
from .domains.branch.router import router as branch_router
from .domains.employee.router import router as employee_router
from .domains.author.router import router as author_router
from .domains.item_author.router import router as item_author_router
from .domains.item_type.router import router as itemtype_router
from .domains.item_details.router import router as item_detail_router
from .domains.reservation.router import router as reservation_router



# API version 1
v1_router = APIRouter(prefix="/api/v1")

# Domain Routers
v1_router.include_router(patron_router)
v1_router.include_router(item_router)
v1_router.include_router(transaction_router)
v1_router.include_router(branch_router)
v1_router.include_router(employee_router)
v1_router.include_router(author_router)
v1_router.include_router(item_author_router)
v1_router.include_router(itemtype_router)
v1_router.include_router(item_detail_router)
v1_router.include_router(reservation_router)


# Main router for the API
api_router = APIRouter()
api_router.include_router(v1_router)
