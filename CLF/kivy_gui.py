from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty

class RootWidget(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.cols = 3

        self.add_widget(Label(text='Enter directory to DICOM files:'))
        self.add_widget(Label(text='Enter Sex (m/f)'))
        self.add_widget(Label(text='Enter Age (18-60)'))

        self.dicomdir_text = TextInput(text='DICOM directory', multiline=False)
        self.add_widget(self.dicomdir_text)

        self.sex_text = TextInput(text='sex', multiline=False)
        # self.sex_text.bind(text=self.update_sex)
        self.add_widget(self.sex_text)

        self.age_text = TextInput(text='age', multiline=False)
        # self.age_text.bind(text=self.update_age)
        self.add_widget(self.age_text)

        self.go_button = Button(text='Go')
        self.go_button.bind(on_touch_down=self.go)
        self.add_widget(self.go_button)


    def go(self, instance, touch):
        '''The code inside the if-block is executed when the go_button is pressed.'''
        if self.go_button.collide_point(*touch.pos):
            print(f"sex: {self.sex_text.text}, age: {self.age_text.text}")


class LesionApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    LesionApp().run()
