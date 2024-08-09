# A small class for handeling notes
# Ideas:

import os

from Tooling.ToolConstructor import *

NOTES_DIR = "Notes"

class NoteTools:
    def make_note_description():
        des = ToolDescription("make_note", "Makes a note with a title and some contents. The tool will return Succes, then title and content, or Failed with an error message if the note title allready exsists")

        des["title", True] = str
        des["content", True] = str

        return des

    def make_note(gpt_args):
        title = gpt_args["title"]
        content = gpt_args["content"]

        # Check if the Notes folder exists, if not, create it
        if not os.path.exists(NOTES_DIR):
            os.makedirs(NOTES_DIR)
        
        # Create the full path for the new note
        file_path = os.path.join(NOTES_DIR, f"{title}.txt")

        if os.path.exists(file_path):
            return "Failed: Note with the given title already exists."
        
        # Write the content to the file
        with open(file_path, "w") as file:
            file.write(content)
        
        return f"Succes: Title '{title}' {file_path}"
