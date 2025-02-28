from fabric import Connection
from astrbot.api.message_components import *
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult,CommandResult
from astrbot.api.star import Context, Star, register
import os
import inspect
import hashlib

from AstrBot.astrbot.core.message.components import Plain

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
            if  "暂停" in event.message_str.strip():
                del self.img_senders[sender]
                yield event.plain_result("已暂停上传")
            else:
                message_obj=event.message_obj
                for i in message_obj.message:

                    if isinstance(i, Image):
                        image_obj = i
                        # yield CommandResult().file_image(image_obj.file)
                        yield event.chain_result([Image.fromFileSystem(image_obj.file)])

                        try:
                            # 获取文件的扩展名和哈希值
                            file_name = os.path.basename(image_obj.file)
                            file_extension = os.path.splitext(file_name)[1]
                            file_hash = self.get_file_hash(image_obj.file)
                            new_file_name = f"{file_hash}{file_extension}"
                            remote_file_path = os.path.join("/root/alist/upload/", sender)
                            conn.run(f"mkdir -p {remote_file_path}")
                            remote_file_path = os.path.join(remote_file_path, new_file_name)
                            
                            conn.put(image_obj.file, remote_file_path)
                            yield event.plain_result("上传成功")
                        except Exception as e:
                            yield event.plain_result(f"上传失败:{str(e)}")
                        break



    @filter.command("upload")
    async def upload_img(self, event: AstrMessageEvent):

        sender = event.get_sender_id()
        if sender not in self.img_senders:
            self.img_senders[sender] = True
            yield event.plain_result("请上传图片")

    def get_file_hash(self,file_path):
        """计算文件的哈希值（使用SHA256）"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()