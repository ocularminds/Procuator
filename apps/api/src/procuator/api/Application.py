from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from procuator import __version__
from procuator.api.ApiController import ApiController
from procuator.api.AppServices import AppServices


class AppFactory:
    """Creates a fully composed FastAPI application."""

    def create(self, services: AppServices | None = None) -> FastAPI:
        appServices = services or AppServices()

        @asynccontextmanager
        async def lifespan(_: FastAPI) -> AsyncIterator[None]:
            try:
                yield
            finally:
                await appServices.close()

        application = FastAPI(
            title="Procuator",
            version=__version__,
            lifespan=lifespan,
        )
        application.state.services = appServices
        application.include_router(ApiController(appServices).createRouter())
        return application


def createApp(services: AppServices | None = None) -> FastAPI:
    return AppFactory().create(services)


app = createApp()
