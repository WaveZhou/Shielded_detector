import src.uis_designer.settings_ui as su
from src.pass_message.settings import Settings
from src.uis_own.run_form_own import *
from PyQt5.QtWidgets import QMessageBox


class UI_form_own(QWidget, su.Ui_Form):
    def next_0_check(self):
        internalArray = [5, 10, 30, 60, 60 * 2, 60 * 5, 60 * 10, 60 * 20]
        if self.bf_name_gui.text() and self.bf_sentence_gui.text():
            Settings.bf_name = self.bf_name_gui.text()
            Settings.bf_sentence = self.bf_sentence_gui.text()
            Settings.check_internal = internalArray[self.check_internal_gui.currentIndex()]
            return True
        return False

    def next_0_bind(self):
        if self.next_0_check():
            self.stackedWidget.setCurrentIndex(1)

    def next_1_check(self):
        Settings.is_jump_out = self.is_jump_out_gui.isChecked()
        Settings.is_sent_to_file_receiver = self.is_sent_to_file_receiver_gui.isChecked()
        Settings.is_inform_brothers = self.is_inform_brothers_gui.isChecked() and self.brother_list_gui.count() > 0 and self.send_to_brother_message.text() != ""
        if Settings.is_inform_brothers:
            Settings.brothers_list = [self.brother_list_gui.item(i).text() for i in
                                      range(self.brother_list_gui.count())]
            Settings.send_to_brother_message = self.send_to_brother_message.text()

    def next_1_bind(self):
        self.stackedWidget.setCurrentIndex(2)

    def next_2_check(self):
        reply_text = self.auto_reply_text_gui.toPlainText()
        Settings.is_auto_reply = self.is_auto_reply_gui.isChecked() and reply_text != ""
        if Settings.is_auto_reply:
            Settings.auto_reply_way_choose = self.auto_reply_way_gui.currentIndex()
            print(Settings.auto_reply_way_choose)
            Settings.auto_reply_content = reply_text.strip().split("\n")

    def next_2_bind(self):
        self.stackedWidget.setCurrentIndex(3)

    def open_message_box(self, str):
        msgBox = QMessageBox()
        msgBox.setText(str)
        msgBox.exec()

    def run_bind(self):
        if not self.next_0_check():
            self.open_message_box("请填写名字和检测内容！")
            self.stackedWidget.setCurrentIndex(0)
            return

        self.next_1_check()
        self.next_2_check()
        Settings.is_close_after_inform = self.is_close_after_inform_gui.isChecked()
        Settings.is_stop_by_filereceiver = self.is_stop_by_filereceiver_gui.isChecked()
        print(Settings.message())
        self.programSignal.settings_done.emit()

    def add_brother(self):
        brother_name = self.brother_name.text()
        if brother_name:
            self.brother_list_gui.addItem(brother_name)
        self.brother_name.setText("")

    def delete_brother(self):
        selectItems = self.brother_list_gui.selectedItems()
        print(selectItems)
        for item in selectItems:
            self.brother_list_gui.takeItem(self.brother_list_gui.row(item))

    def connect(self):
        self.next_0_btn.clicked.connect(self.next_0_bind)
        self.next_1_btn.clicked.connect(self.next_1_bind)
        self.next_2_btn.clicked.connect(self.next_2_bind)
        self.add_brother_btn.clicked.connect(self.add_brother)
        self.delete_brother_btn.clicked.connect(self.delete_brother)
        self.run_btn.clicked.connect(self.run_bind)

    def hide_something(self):
        self.add_brother_widget.hide()
        self.widget_2.hide()

    def setupUi(self):
        super().setupUi(self)
        self.connect()
        self.hide_something()

    def __init__(self, programSignal):
        super().__init__()
        self.programSignal = programSignal
