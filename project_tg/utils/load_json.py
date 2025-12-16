import asyncio
import json
from uuid import UUID
from datetime import datetime
from core.model import Video, VideoSnapshots, db_helper_conn


async def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    async with db_helper_conn.get_generator_session() as session:
        for v in data["videos"]:
            video = Video(
                id=UUID(v["id"]),
                creator_id=UUID(v["creator_id"]),
                video_created_at=datetime.fromisoformat(v["video_created_at"]),
                views_count=v["views_count"],
                likes_count=v["likes_count"],
                comments_count=v["comments_count"],
                reports_count=v["reports_count"],
            )
            session.add(video)

            for s in v["snapshots"]:
                snap = VideoSnapshots(
                    id=UUID(s["id"]),
                    video_id=UUID(s["video_id"]),
                    views_count=s["views_count"],
                    likes_count=s["likes_count"],
                    comments_count=s["comments_count"],
                    reports_count=s["reports_count"],
                    delta_views_count=s["delta_views_count"],
                    delta_likes_count=s["delta_likes_count"],
                    delta_comments_count=s["delta_comments_count"],
                    delta_reports_count=s["delta_reports_count"],
                    created_at=datetime.fromisoformat(s["created_at"]),
                    updated_at=datetime.fromisoformat(s["updated_at"]),
                )
                session.add(snap)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(load_json("videos.json"))
