from fabric import Connection
from astrbot.api.message_components import *
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult,CommandResult
from astrbot.api.star import Context, Star, register
from io import BytesIO
import inspect
host = "31.56.123.4"
username = "root"
conn = Connection(host=host, user=username, connect_kwargs={"password": "Qwer3866373"})
@register("fish_countapiimg", "案板上的鹹魚", "计算服务器中有的图片数量", "1.0")
class Countimg(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.img_senders={}

    @filter.command("cimg")
    async def get_countimg(self, event: AstrMessageEvent):
        res=0
        result = conn.run("ls -l /root/random-api/portrait/NON-H | wc -l", hide=True)
        res+=int(result.stdout.strip())
        result = conn.run("ls -l /root/random-api/landscape/NON-H | wc -l", hide=True)
        res += int(result.stdout.strip())
        yield event.plain_result(f"总计{res}张图")

    @filter.command("cimgh")
    async def get_countimgh(self, event: AstrMessageEvent):
        res = 0
        result = conn.run("ls -l /root/random-api/portrait/H | wc -l", hide=True)
        res += int(result.stdout.strip())
        result = conn.run("ls -l /root/random-api/landscape/H | wc -l", hide=True)
        res += int(result.stdout.strip())
        yield event.plain_result(f"总计{res}张涩图")

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def handel_upload(self,event: AstrMessageEvent):
        sender=event.get_sender_id()
        if sender  in self.img_senders:
            message_obj=event.message_obj
            for i in message_obj.message:
                if isinstance(i, Image):
                    image_obj = i
                    yield CommandResult().file_image(image_obj.file)
                    break

    @filter.command("upload")
    async def upload_img(self, event: AstrMessageEvent):
        yield event.plain_result(inspect.getsource(CommandResult))
        sender = event.get_sender_id()
        if sender not in self.img_senders:
            self.img_senders[sender] = True
            yield event.plain_result("请上传图片")
