from typing import Final, Literal

URL: Final[str] = 'https://x.com/elonmusk?mx=2'

SEARCH_PATTERN: Final[str] = 'UserTweets'

BROWSER_RETRY_TIMES: Final[int] = 0

RETRY_TIMES: Final[int] = 10

TIMEOUT_SENDING: Final[int] = 150

DEFAULT_USER_AGENT: Final[str] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:129.0) Gecko/20100101 Firefox/129.0'

DEFAULT_HEADERS: Final[dict[str, str]] = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

BROWSER_INIT_ARGS: Final[list[str]] = [
    '--no-zygote',
    '--no-sandbox',
    '--disable-gpu',
    '--single-process',
    '--disable-infobars',
    '--window-position=0,0',
    '--disable-dev-shm-usage',
    '--disable-setuid-sandbox',
    '--ignore-certificate-errors',
    '--ignore-certificate-errors-spki-list',
    '--disable-blink-features=AutomationControlled',
    '--disable-features=IsolateOrigins,site-per-process',
]

VIEWPORT: Final[dict[str, int]] = {'width': 1920, 'height': 1080}

DEFAULT_GEOLOCATION: Final[dict[str, float]] = {'longitude': 12.4924, 'latitude': 41.8902}

DEFAULT_PERMISSIONS: Final[list[str]] = ['geolocation']
DEFAULT_LOCALE: Final[str] = 'en-US'
WAIT_UNTIL: Literal[str] = 'domcontentloaded'

STEALTH_SCRIPT: Final[str] = """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.navigator.chrome = {
                runtime: {},
                // Add more properties if necessary
            };
            // Add more overrides as necessary
        """
