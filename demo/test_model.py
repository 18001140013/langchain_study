from threading import Thread

import wx
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

"""
小Demo实现本地模型对话：
"""


class ChatFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="本地Ollama对话", size=(600, 500))
        panel = wx.Panel(self)

        # 聊天展示框
        self.chat_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.VSCROLL)
        self.chat_ctrl.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # 输入框
        self.input_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.send_btn = wx.Button(panel, label="发送")
        self.send_btn.Bind(wx.EVT_BUTTON, self.on_send)

        # 布局
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.chat_ctrl, proportion=3, flag=wx.EXPAND | wx.ALL, border=8)
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(self.input_ctrl, proportion=1, flag=wx.EXPAND | wx.RIGHT, border=8)
        row_sizer.Add(self.send_btn)
        sizer.Add(row_sizer, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=8)
        panel.SetSizer(sizer)

        # 初始化本地模型
        self.llm = init_chat_model(
            model="deepseek-r1:7b",
            model_provider="ollama",
            base_url="http://localhost:11434",
            temperature=0.7
        )

    # 界面追加一条消息
    def append_text(self, text):
        wx.CallAfter(self.on_append_text, text)

        # 子线程执行一个主函数

    def call_after(self, text):
        wx.CallAfter(self.on_append_text, text)

    # 界面追加一条消息
    def on_append_text(self, text):
        self.chat_ctrl.AppendText(text)
        self.chat_ctrl.SetInsertionPointEnd()  # 自动滚动到末尾

    def on_send(self, event):
        user_text = self.input_ctrl.GetValue().strip()
        if not user_text:
            return
        self.chat_ctrl.AppendText(f"\n【你】：{user_text}\n【模型】：")
        self.input_ctrl.SetValue("")
        self.send_btn.Disable()

        Thread(target=self.on_run, args=(user_text,)).start()

    def on_run(self, user_text):
        try:
            # 流式返回
            stream = self.llm.stream([HumanMessage(content=user_text)])
            for chunk in stream:
                if chunk.content:
                    self.append_text(chunk.content)

            self.append_text("\n")
        except Exception as e:
            self.append_text(f"\n出错：{e}\n")
        finally:
            wx.CallAfter(self.send_btn.Enable)


if __name__ == "__main__":
    app = wx.App(False)
    frame = ChatFrame()
    frame.Show()
    app.MainLoop()
