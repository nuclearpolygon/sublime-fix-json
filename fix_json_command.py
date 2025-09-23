import sublime
import sublime_plugin
import re
import json

def is_valid_json(match):
    matched_group = match.group(1)
    try:
        json.loads(matched_group)
        return matched_group
    except ValueError:
        return match.group(0)

def process_text(text):
    try:
        d = json.loads(text)
        sublime.status_message("JSON is valid. Formatting...")
        return json.dumps(d, indent=4)
    except ValueError:
        pass

    # Newlines
    text = re.sub(r'\n', '', text)
    # Stringified json
    text = re.sub(r"'({.*?})'", is_valid_json, text)
    # Single quotes
    text = re.sub(r"'", r'"', text)
    # Unquoted paths-like strings
    text = re.sub(r': (?!True|False|None|\d+(?:\.\d+)?)([/\w\\. #@:$%]+)([,}])', r': "\g<1>"\g<2>', text)
    # None, True, False
    text = re.sub('None', 'null', text)
    text = re.sub('True', 'true', text)
    text = re.sub('False', 'false', text)
    try:
        d = json.loads(text)
        return json.dumps(d, indent=4)
    except ValueError as e:
        print(e)
        sublime.status_message("Could not fix json!")
        return None

class FixJsonCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get all text from the current view (tab)
        entire_region = sublime.Region(0, self.view.size())
        text = self.view.substr(entire_region)
        processed_text = process_text(text)
        if processed_text:
            self.view.replace(edit, entire_region, processed_text)
            sublime.status_message("JSON fixed successfully!")
            self.view.set_syntax_file('Packages/JSON/JSON.sublime-syntax')