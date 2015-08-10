"""
???
"""

"""
import urllib, datetime, json, csv, utils

from xblock.core import XBlock
from xblock.fields import Scope, Integer, List, String, Boolean, Dict
from xblock.fragment import Fragment

from django.template import Context, Template
"""

import urllib, datetime, json, csv, utils
from .utils import render_template, load_resource, resource_string
from django.template import Context, Template
from xblock.core import XBlock
from xblock.fields import Scope, Integer, List, String, Boolean, Dict
from xblock.fragment import Fragment

class LMSManipulatorXBlock(XBlock):

    display_name = String(
        default="LMS Manipulator",
        display_name="LMSManipulator XBlock",
        help="",
        scope=Scope.settings
    )

    course_url = String(
        default="",
        help="Course URL. Mandatory field.",
        scope=Scope.content
    )

    hide_nav_buttons = Boolean(
        default=False,
        help="Hide top navigation buttons in LMS",
        scope=Scope.content
    )

    hide_nav = Boolean(
        default=False,
        help="Hide the entire navigation bar in LMS.",
        scope=Scope.content
    )

    hide_sequence_bottom = Boolean(
        default=False,
        help="Hide bottom navigation buttons in LMS",
        scope=Scope.content
    )

    hide_sidebar = Boolean(
        default=False,
        help="Hide side bar in LMS",
        scope=Scope.content
    )

    toggle_sidebar = Boolean(
        default=False,
        help="Toggle side bar in LMS",
        scope=Scope.content
    )

    csv_url = String(
        default="",
        help="URL to CSV containing slide ids and default states",
        scope=Scope.content
    )

    dev_stuff = Boolean(
        help="Show chx_dev_stuff div in LMS?",
        default=False, scope=Scope.content
    )

    course_tree = List(
        help="List containing course tree read from specified CSV file",
        default=[], scope=Scope.content
    )

    course_tree_student = List(
        help="List containing course tree adapted to the student's performance and progress",
        default=[], scope=Scope.user_state
    )

    @XBlock.json_handler
    def lmx_init(self, data, suffix=''):

        #self.session_ended = False

        #settings = {
            #"tick_interval": self.tick_interval,
        #}

        settings = {}

        return settings

    @XBlock.json_handler
    def refresh_sequence(self, data, suffix=''):

        content = {"csv_object": ""}

        return content

#    @staticmethod
#    def clear_data(self):
#        del self.sessions[:]

    #def redirect()

    def student_view(self, context=None):
        """
        The LMS view
        """

        fragment = Fragment()
        content = {'self': self}

        fragment.add_content(render_template('templates/lmsmanipulator.html', content))
        fragment.add_css(load_resource("static/css/lmsmanipulator.css"))
        fragment.add_javascript(render_template('static/js/lmsmanipulator.js', content))
        fragment.initialize_js('LMSManipulatorXBlock')

        return fragment

    def studio_view(self, context=None):
        """
        The CMS view
        """

        fragment = Fragment()
        content = {'self': self}

        fragment.add_content(render_template('templates/lmsmanipulator_edit.html', content))
        fragment.add_css(load_resource('static/css/lmsmanipulator_edit.css'))
        fragment.add_javascript(load_resource('static/js/lmsmanipulator_edit.js'))
        fragment.initialize_js('LMSManipulatorXBlockStudio')

        return fragment

    @XBlock.json_handler
    def studio_save(self, data, suffix=''):
        """
        Course author pressed the Save button in Studio
        """

        result = {'result': 'success'}

        if len(data) > 0:

            self.display_name = data["display_name"]
            self.course_url = data["course_url"]
            self.hide_nav_buttons = data["hide_nav_buttons"] == 1
            self.hide_nav = data["hide_nav"] == 1
            self.hide_sequence_bottom = data["hide_sequence_bottom"] == 1
            self.hide_sidebar = data["hide_sidebar"] == 1
            self.toggle_sidebar = data["toggle_sidebar"] == 1
            self.dev_stuff = data["dev_stuff"] == 1

            if self.hide_sidebar:
                self.toggle_sidebar = False

            self.csv_url = data["csv_url"]

            # Generate course tree

            if self.csv_url[:4] == "http" and self.csv_url[-3:] == "csv":

                '''
                states
                vc - visible, but must complete
                hc - hidden, but must complete
                vs - visible, but skippable (default if column is blank)
                hs - hidden, but skippable when visible
                '''

                print ("-----" + self.csv_url)

                try:

                    f = urllib.urlopen(self.csv_url)

                    cr = csv.reader(f)

                    for r in cr:
                        print (r)

                    f.close()

                except:
                    print ("CSV reading error.")

        return result

    @staticmethod
    def workbench_scenarios():
        return [
            ("LMSManipulatorXBlock",
             """<vertical_demo>
                <lmsmanipulator/>
                </vertical_demo>
             """),
        ]