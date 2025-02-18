from fabric import Connection
from astrbot.api.message_components import *
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
@register("fish_countapiimg", "案板上的鹹魚", "计算服务器中有的图片数量", "1.0")
host = "31.56.123.4"
username = "root"

conn = Connection(host=host, user=username, connect_kwargs={"password": "Qwer3866373"})
print(result.stdout)
class Countimg(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("cimg")
    async def get_countimg(self, event: AstrMessageEvent):
        result = conn.run("ls -l /root/random-api/portrait/NON-H | wc -l", hide=True)
        yield event.plain_result(result.stdout)
