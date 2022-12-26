import asyncio
import uuid
from typing import List

import asyncpg
from faker import Faker

from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.db.repositories.comments import CommentsRepository
from app.db.repositories.items import ItemsRepository
from app.db.repositories.users import UsersRepository
from app.models.domain.comments import Comment
from app.models.domain.items import Item
from app.models.domain.profiles import Profile
from app.models.domain.users import User
from app.services.items import get_slug_for_item

user_repo: UsersRepository = get_repository(UsersRepository)
item_repo: ItemsRepository = get_repository(ItemsRepository)
comments_repo: CommentsRepository = get_repository(CommentsRepository)

fake = Faker()

config = get_app_settings()


async def create_pool():
    pool = await asyncpg.create_pool(
        dsn=config.database_url,
    )
    return pool


_pool = asyncio.get_event_loop().run_until_complete(create_pool())


def generate_users() -> List[User]:
    users = []
    for _ in range(100):
        users.append(
            User(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                bio=fake.text(),
            )
        )
    return users


def _generate_profile():
    return Profile(
        bio=fake.text(),
        following=False,
        username=fake.user_name()
    )


def generate_items() -> List[Item]:
    items = []
    for _ in range(100):
        _title = fake.sentence()
        _tags = [fake.word() for _ in range(3)]
        items.append(
            Item(
                title=_title,
                description=fake.text(),
                price=fake.pyfloat(),
                slug=get_slug_for_item(_title),
                tags=_tags,
                seller=_generate_profile(),
                favorited=False,
                favorites_count=0
            )
        )
    return items


def generate_comments() -> List[Comment]:
    comments = []
    for _ in range(100):
        comments.append(
            Comment(
                body=fake.text(),
                seller=_generate_profile(),
            )
        )
    return comments


async def create_user(user: User):
    async with _pool.acquire() as conn:
        return await user_repo(conn).create_user(
            username=user.username,
            email=user.email,
            password=str(uuid.uuid4()),
        )


async def create_item(item: Item, user: User):
    async with _pool.acquire() as conn:
        return await item_repo(conn).create_item(
            title=item.title,
            description=item.description,
            seller=user,
            slug=item.slug
        )


async def create_comment(comment: Comment, user: User, item: Item):
    async with _pool.acquire() as conn:
        return await comments_repo(conn).create_comment_for_item(
            body=comment.body,
            item=item,
            user=user,
        )


async def main():
    users = generate_users()
    items = generate_items()
    comments = generate_comments()

    for user, item, comment in zip(users, items, comments):
        await create_user(user)
        await create_item(item, user)
        await create_comment(comment, user, item)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    exit(0)
