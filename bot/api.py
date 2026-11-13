import logging

import aiohttp

from bot.config import API_TOKEN, API_URL

logger = logging.getLogger(__name__)


async def save_feedback(payload: dict) -> bool:
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.post(API_URL, json=payload, headers={'X-Api-Token': API_TOKEN}) as response:
                if response.status == 201:
                    return True
                logger.warning('API %s qaytardi: %s', response.status, await response.text())
    except (aiohttp.ClientError, TimeoutError) as error:
        logger.warning('API bilan aloqa yo\'q: %s', error)
    return False
