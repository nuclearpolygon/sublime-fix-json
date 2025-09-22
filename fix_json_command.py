import sublime
import sublime_plugin
import re
import json

def is_valid_json(match):
    matched_group = match.group(1)
    try:
        json.loads(matched_group)
        print('REPLACE')
        return matched_group
    except:
        print('SKIP')
        return match.group(0)

def fix_json(text):
    try:
        d = json.loads(text)
        return json.dumps(d, indent=4)
    except ValueError:
        print('Not a valid json. fixing')

    text = re.sub(r'\n', '', text)
    text = re.sub(r"'({.*?})'", is_valid_json, text)
    text = re.sub(r"'", r'"', text)
    text = re.sub(r': (?!True|False|None|\d+(?:\.\d+)?)([/\w\\. #@$%]+)([,}])', r': "\g<1>"\g<2>', text)
    text = re.sub('None', 'null', text)
    text = re.sub('True', 'true', text)
    text = re.sub('False', 'false', text)
    try:
        d = json.loads(text)
        return json.dumps(d, indent=4)
    except ValueError:
        return text


class FixJsonCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get all text from the current view (tab)
        entire_region = sublime.Region(0, self.view.size())
        current_text = self.view.substr(entire_region)
        
        # Process the text through your fix_json function
        fixed_text = fix_json(current_text)
        
        # Replace the entire content with fixed text
        self.view.replace(edit, entire_region, fixed_text)
        self.view.set_syntax_file('Packages/JSON/JSON.sublime-syntax')
        
        # Show completion message
        sublime.status_message("JSON fixed successfully!")