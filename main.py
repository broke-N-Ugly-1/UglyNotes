import time

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from kivy.storage.jsonstore import JsonStore

Builder.load_file("main.kv")
notes_db = JsonStore("notes.json")

class NewNote(Popup):
	
	def create_note(self, note):
		if len(note.text.strip()) > 0:
			id = 0
			if notes_db.keys() != []:
				id = int(notes_db.keys()[-1]) + 1
			data = note.text.strip()
			notes_db.put(key=f"{id}", note=data)
			self.dismiss()
		else:
			note.text = ""
			note.hint_text = "Cannot create empty note"

class Note(BoxLayout):
	note_ids = []

	def __init__(self, id, data, **kwargs):
		super().__init__(**kwargs)
		Note.note_ids.append(self)
		self.ids['data'].text = data

	def delete(self, note, *args):
		#works but not everytime, work on it later
		"""
			tips
		find a way to sync the ids in the store with the widgets
		"""
		try:
			id = Note.note_ids.index(note)
			notes_db.delete(key=str(id))
		except Exception as e:
			print(e)

class AppLayout(Screen):

	def __init__(self, **kw):
		super().__init__(**kw)
		self.ids["notes_board"].bind(minimum_height=self.ids['notes_board'].setter('height'))
		self.refresh()
	
	def create_note(self, *args):
		NewNote().open()

	def refresh(self, *args):
		notes = notes_db.keys()
		Note.note_ids = []
		self.ids['notes_board'].children = []
		self.ids['notes_board'].add_widget(Label(text="Welcome to uglyNotES", padding=5, size_hint_y=None, height=40))
		self.ids['notes_board'].add_widget(Label(text=f"{time.ctime().split()[0]}, {time.ctime().split()[1]} {time.ctime().split()[-1]}", padding=5, size_hint_y=None, height=40))
		if len(notes) != 0:
			for id, note in enumerate(notes):
				note = Note(id=id, data=notes_db.get(note)["note"])
				self.ids['notes_board'].add_widget(note)

	def on_touch_move(self, touch):
		self.refresh()

class UglyNotesApp(App):
	def build(self):
		return AppLayout()

UglyNotesApp().run()