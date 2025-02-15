import asyncio
import logging
from typing import Any
from asyncio import sleep
from random import uniform
from contextlib import suppress
from logging import StreamHandler

from playwright.async_api import (
    Browser, BrowserContext, Page, Playwright, async_playwright, Response
)

import consts

from parser import Parser
from handler import create_handler


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Crawler:
    Parser: Parser = Parser(logger=logger)

    def __init__(self, headless_mode: bool = True):
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self.headless_mode: bool = headless_mode
        self.pw: Playwright | None = None

    async def capture_response(self, response: Response) -> None:
        if consts.SEARCH_PATTERN in response.url:
            logger.info(f'Response from request: {response.url}')
            await self.Parser.convert_data(response=response)

    async def launch_browser(self, url: str) -> None:
        logger.info('Launching browser...')
        try:
            async with async_playwright() as self.pw:
                self.browser: Browser = await self.pw.chromium.launch(
                    headless=self.headless_mode,
                    args=consts.BROWSER_INIT_ARGS
                )
                self.context = await self.browser.new_context(
                    viewport=consts.VIEWPORT,
                    java_script_enabled=True,
                    ignore_https_errors=True,
                    locale=consts.DEFAULT_LOCALE,
                )
                self.page: Page = await self.context.new_page()
                self.page.on(event='response', f=self.capture_response)

                await self.open_url(url=url)

                logger.info(
                    f'Browser launched successfully in headless mode for {self.__class__.__name__}'
                    if self.headless_mode else f'Browser launched successfully in headed mode'
                )
        except Exception as e:
            logger.error(f'Failed to launch browser: {e!r}')

    async def _stealth(self) -> None:
        if not self.context:
            logger.error('BrowserContext is not initialized.')
            return
        await self.context.add_init_script(script=consts.STEALTH_SCRIPT)

    async def open_url(self, url: str, min_sleep: int = 1, max_sleep: int = 3) -> None:
        try:
            await self.page.goto(url=url)  # noqa
            await self.page.wait_for_load_state(consts.WAIT_UNTIL)
            await self._stealth()
            await sleep(uniform(min_sleep, max_sleep))
            logger.info(f'Navigated to URL: {url}')
        except Exception as e:
            logger.error(f'Failed to navigate to URL {url}: {e!r}')


    async def close(self) -> None:
        try:
            if self.browser:
                await self.browser.close()
            if self.pw:
                await self.pw.stop()
            logger.info('Browser closed successfully')
        except Exception as e:
            logger.error(f'Failed to close the browser: {e!r}')

    async def start_browser(
        self,
        url: str,
        retry_times: int = consts.BROWSER_RETRY_TIMES
    ) -> Any:
        with suppress(Exception):
            await self.launch_browser(url=url)
        if retry_times:
            return await self.start_browser(retry_times=retry_times - 1, url=url)

    async def main(self) -> None:
        console_handler: StreamHandler = create_handler()
        logger.addHandler(console_handler)

        await self.start_browser(url=consts.URL)
        await sleep(0.3)
        await self.close()


if __name__ == '__main__':
    asyncio.run(Crawler().main())
