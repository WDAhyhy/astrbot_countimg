from fabric import Connection
from astrbot.api.message_components import *
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
host = "31.56.123.4"
username = "root"
conn = Connection(host=host, user=username, connect_kwargs={"password": "Qwer3866373"})
@register("fish_countapiimg", "案板上的鹹魚", "计算服务器中有的图片数量", "1.0")
class Countimg(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("cimg")
    async def get_countimg(self, event: AstrMessageEvent):
        res=0
        result = conn.run("ls -l /root/random-api/portrait/NON-H | wc -l", hide=True)
        res+=int(result.stdout.strip())
        result = conn.run("ls -l /root/random-api/landscape/NON-H | wc -l", hide=True)
        res += int(result.stdout.strip())
        yield event.plain_result(f"总计{res}张图")

    # @filter.command("cimgh")
    # async def get_countimgh(self, event: AstrMessageEvent):
    #     res = 0
    #     result = conn.run("ls -l /root/random-api/portrait/H | wc -l", hide=True)
    #     res += int(result.stdout.strip())
    #     result = conn.run("ls -l /root/random-api/landscape/H | wc -l", hide=True)
    #     res += int(result.stdout.strip())
    #     yield event.plain_result(f"总计{res}张涩图")
