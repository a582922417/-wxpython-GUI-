import wx
from static import setting
from math import ceil
import threading
from view.swf import *

TextCtrl = 0


class Frame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, pos=(200, 200), size=(720, 600),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        global TextCtrl
        # 页面组件
        self.sub_text_li = []
        self.sub_ctrl_li = []
        self.tab_button_li = []
        self.page_num = 0
        self.now_tab_text = ''
        # 容纳其他组件的容器
        self.panel = wx.Panel(self)
        self.TextCtrl = wx.TextCtrl(self.panel, value="", size=(665, 250), pos=(20, 300),
                                    style=wx.TE_MULTILINE)
        TextCtrl = self.TextCtrl
        # 获取data
        self.res_array = setting.res_array
        self.max_page = ceil(len(self.res_array) / 5)
        # 遍历data
        self.get_tab_button()
        # 提交
        self.submit = wx.Button(self.panel, -1, '执行', size=(120, 40), pos=(580, 250))
        # 菜单翻页
        self.pre_page = wx.Button(self.panel, -1, '上一页', size=(50, 20), pos=(310, 0))
        self.next_page = wx.Button(self.panel, -1, '下一页', size=(50, 20), pos=(360, 0))
        # 设置点击事件
        self.Bind(wx.EVT_BUTTON, self.subMit, self.submit)
        self.Bind(wx.EVT_BUTTON, self.prePage, self.pre_page)
        self.Bind(wx.EVT_BUTTON, self.nextPage, self.next_page)

    def onClick(self, event):
        # 清除控件
        # self.TextCtrl.Clear()
        for sub_text in self.sub_text_li:
            sub_text.Destroy()
        for sub_ctrl in self.sub_ctrl_li:
            sub_ctrl.Destroy()
        if self.sub_text_li:
            self.sub_text_li = []
            self.sub_ctrl_li = []
        for data_list in self.res_array:
            button = event.GetEventObject()
            column_num = 0
            row_num = 0
            # 渲染菜单按钮
            if data_list[0] == button.GetLabel():
                variable_name_li = data_list[2].split(',')
                variable_default_li = data_list[4].split(',')
                # 渲染控件
                for index, variable_name in enumerate(variable_name_li):
                    # 一页展示最多5个按钮
                    if index != 0 and index % 5 == 0:
                        column_num += 1
                        row_num = 0
                    sub_text = wx.StaticText(self.panel, -1, variable_name,
                                             ((column_num * 300) + 20, (row_num * 40) + 100))
                    self.sub_text_li.append(sub_text)
                    sub_ctrl = wx.TextCtrl(self.panel, value='', size=(120, 25),
                                           pos=((column_num * 300) + 100, (row_num * 40) + 95))
                    sub_ctrl.AppendText(variable_default_li[index])
                    self.sub_ctrl_li.append(sub_ctrl)
                    row_num += 1
        # 当前选项卡
        self.now_tab_text = wx.StaticText(self.panel, -1, event.GetEventObject().GetLabel(),
                                          (300, 60))
        self.sub_text_li.append(self.now_tab_text)

    # 上一页
    def prePage(self, event):
        if self.page_num == 0:
            return ''
        else:
            # 清除控件
            for sub_text in self.sub_text_li:
                sub_text.Destroy()
            for sub_ctrl in self.sub_ctrl_li:
                sub_ctrl.Destroy()
            for tab_button in self.tab_button_li:
                tab_button.Destroy()
            if self.sub_text_li:
                self.sub_text_li = []
                self.sub_ctrl_li = []
            if self.tab_button_li:
                self.tab_button_li = []
            self.page_num -= 1
            self.get_tab_button()

    # 下一页
    def nextPage(self, event):
        if self.page_num == self.max_page:
            return ''
        else:
            # 清除控件
            for sub_text in self.sub_text_li:
                sub_text.Destroy()
            for sub_ctrl in self.sub_ctrl_li:
                sub_ctrl.Destroy()
            for tab_button in self.tab_button_li:
                tab_button.Destroy()
            if self.sub_text_li:
                self.sub_text_li = []
                self.sub_ctrl_li = []
            if self.tab_button_li:
                self.tab_button_li = []
            self.page_num += 1
            self.get_tab_button()

    # 遍历data
    def get_tab_button(self):
        # 遍历data
        for index, data_list in enumerate(self.res_array[self.page_num:self.page_num + 5]):
            # 动态生成按钮
            exec('self.{0} = wx.Button(self.panel, -1, data_list[0], size=(120, 40), pos=(index * 150, 20))'.format(
                data_list[3]))
            # 设置点击事件
            self.Bind(wx.EVT_BUTTON, self.onClick, getattr(self, data_list[3]))
            getattr(self, data_list[3]).SetDefault()
            self.tab_button_li.append(getattr(self, data_list[3]))

    def subMit(self, event):
        # self.TextCtrl.Clear()
        data_dic = {'TextCtrl': self.TextCtrl}
        try:
            now_tab = self.now_tab_text.GetLabel()
        except Exception as e:
            self.TextCtrl.AppendText('\n请选择执行项')
            return None

        for data_list in self.res_array:
            variable_li = data_list[1].split(',')
            if data_list[0] == now_tab:
                for index, item in enumerate(variable_li):
                    if self.sub_ctrl_li[index].GetValue():
                        data_dic[item] = self.sub_ctrl_li[index].GetValue()
                    else:
                        # 必填校验
                        self.TextCtrl.AppendText('\n请录入必填项{0}'.format(item))
                        return None
                exec("threading.Thread(target={0}, kwargs=data_dic).start()".format(data_list[3]))
                self.TextCtrl.AppendText('\n{0}开始执行'.format(data_list[0]))
                return None


if __name__ == '__main__':
    # 创建一个应用程序对象，用于消息循环
    app = wx.App()
    # 创建一个窗体
    frame = Frame(None, "CallCenterAT")
    frame.Show()
    app.MainLoop()
