__all__ = ("master_router", )

from aiogram import Router

from .timer_handlers import router as timer_router
from .command_handlers import router as command_router
from .message_handlers import router as message_router
from .callback_handlers import router as callback_router

master_router = Router(name=__name__)

master_router.include_routers(
    callback_router,
    timer_router,
    command_router,
    message_router
)
