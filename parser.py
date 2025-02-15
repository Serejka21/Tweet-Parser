import json
from logging import Logger

from typing_extensions import Any
from playwright.async_api import Response


class Parser:
    def __init__(self, logger: Logger):
        self.data_collection: list[dict | None] = []
        self.logger: Logger = logger

    async def _save_json(self) -> None:
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(self.data_collection, file, indent=4)

    async def get_pinned_twit(self, tweet: dict) -> None:
        self.data_collection.append(
            {
                'created_ad': tweet.get('created_at', ''),
                'full_text': tweet.get('full_text', ''),
                'favorites': tweet.get('favorite_count', ''),
                'quote_count': tweet.get('quote_count', ''),
                'retweet_count': tweet.get('retweet_count', ''),
                'reply_count': tweet.get('reply_count', ''),
            }
        )

    async def get_profile_info(self, tweet_data: dict) -> None:
        if profile := tweet_data.get('core').get('user_results').get('result').get('legacy'):
            self.data_collection.append(
            {
                'name': profile.get('name'),
                'screen_name': profile.get('screen_name'),
                'followers': profile.get('followers_count'),
                'favourites': profile.get('favourites_count'),
                'friends': profile.get('friends_count'),
                'listed_count': profile.get('listed_count'),
                'profile_image': profile.get('profile_image_url_https'),
            }
        )

    async def get_tweet_info(self, content_data: dict[str, dict]) -> None:
        tweet: dict[str, str] = {
            'created_ad': content_data.get('created_at', ''),
            'full_text': content_data.get('full_text', ''),
            'favorites': content_data.get('favorite_count', ''),
            'quote_count': content_data.get('quote_count', ''),
            'retweet_count': content_data.get('retweet_count', ''),
            'reply_count': content_data.get('reply_count', ''),
        }

        if media := content_data.get('entities', {}).get('media', {}):
            tweet['media'] = media[0].get('media_url_https', '')
        self.data_collection.append(tweet)

    async def process_posts(self, post_list: list[dict] | None) -> None:
        if not post_list:
            return
        for entity in post_list[:50]:
            content_data: dict[str, dict] = (entity.get('content', {}).get('itemContent').
                                             get('tweet_results', {}).get('result', {}).get('legacy'))
            await self.get_tweet_info(content_data=content_data)

    async def process_pinned_twit(self, tweet_data: dict) -> None:
        if not tweet_data:
            return
        main_info: dict[str, dict] = (
            tweet_data.get('entry', {}).get('content', {}).get('itemContent', {}).
            get('tweet_results', {}).get('result', {})
        )
        await self.get_profile_info(tweet_data=main_info)
        await self.get_pinned_twit(tweet=main_info.get('legacy', {}))

    async def process_data(self, data: dict[Any, Any]) -> None:
        timeline: list[dict] | dict = (data.get('data', {}).get('user', {}).get('result', {}).
                                       get('timeline_v2', {}).get('timeline', {}).get('instructions', {}))
        if timeline:
            timeline.pop(0)
            await self.process_pinned_twit(tweet_data=timeline[0])
            await self.process_posts(post_list=timeline[1].get('entries', []))
        if self.data_collection:
            await self._save_json()

    async def convert_data(self, response: Response) -> None:
        try:
            body: bytes = await response.body()
            body_str: str = body.decode('utf-8')
            data: dict[str, dict] = json.loads(body_str)
            self.logger.info(f'Get data: {[key for key in data.keys()]}')
        except Exception as exc:
            self.logger.error(f'Error process response data: {exc!r}')
        else:
            await self.process_data(data=data)
            self.logger.info(f'Data collected: {self.data_collection}')
