from .base import MediaHandler

class PhotoHandler(MediaHandler):
    async def handle(self) -> bool:
        if not self.update.message.photo:
            return False
            
        timestamp, username = self.get_file_metadata()
        photo = self.update.message.photo[-1]
        file = await self.context.bot.get_file(photo.file_id)
        await self.save_file(file, f"{timestamp}_{username}_photo.jpg")
        return True

class VideoHandler(MediaHandler):
    async def handle(self) -> bool:
        if not self.update.message.video:
            return False
            
        timestamp, username = self.get_file_metadata()
        video = self.update.message.video
        file = await self.context.bot.get_file(video.file_id)
        extension = video.mime_type.split('/')[-1]
        await self.save_file(file, f"{timestamp}_{username}_video.{extension}")
        return True

class DocumentHandler(MediaHandler):
    async def handle(self) -> bool:
        if not self.update.message.document:
            return False
            
        timestamp, username = self.get_file_metadata()
        doc = self.update.message.document
        file = await self.context.bot.get_file(doc.file_id)
        await self.save_file(file, f"{timestamp}_{username}_{doc.file_name}")
        return True 