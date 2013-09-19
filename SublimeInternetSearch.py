# Sublime Text 3 API 
import sublime, sublime_plugin 
# for opening URLs`
import webbrowser 
# for text manipulation
import textwrap

# API for search throught Internet 
from .sublime_internet_search import search_manager

class SublimeInternetSearchCommand(sublime_plugin.WindowCommand): 
    """For searching through the Internet"""
    
    def run(self):    
        """Command invocation"""    

        try: 
            if not (hasattr(self, 'search_manager') and self.search_manager is not None): 
                self.search_manager = search_manager.SearchManager()

            # try to configure search manager
            settings = sublime.load_settings('SublimeInternetSearch.sublime-settings')
            self.search_manager.try_configure(settings)

            # input panel
            self.window.show_input_panel('Search:', '', self.on_user_input_done, None, None)        

        except search_manager.ConfigurationError as e: 
            sublime.error_message('SublimeInternetSearch: "' + str(e) + '"')
    
    def on_user_input_done(self, user_input):   
        """Callback for user input panel"""

        try: 
            # search
            search_result = self.search_manager.search(query=user_input)
            self.last_search_result = search_result 

            # format 
            messages = self.__format_result_for_quick_panel(search_result)

            # display
            self.window.show_quick_panel(messages, self.on_user_quick_panel_done, sublime.MONOSPACE_FONT)

        except (search_manager.ConfigurationError, search_manager.SearchError) as e: 
            sublime.error_message('SublimeInternetSearch: "' + str(e) + '"')

    def on_user_quick_panel_done(self, selected_index):  
        """Callback for user quick panel"""
        
        if selected_index == -1: 
            return 

        selected_url = self.last_search_result[selected_index].url        
        webbrowser.open(selected_url)

    def __format_result_for_quick_panel(self, search_result): 
        # max line length at the quick panel
        panel_row_len = 80 - 1 
        panel_row_count_for_description = 1

        def render_item(item): 
            """Renders one item for quick panel"""      

            message = [item.title, item.url]
            for part in textwrap.wrap(item.description, panel_row_len)[:panel_row_count_for_description]: 
                message.append(part)
            return message

        messages = []
        for item in search_result:
            messages.append(render_item(item))
            
        return messages