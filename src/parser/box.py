"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import logging

from utils import Utils
from urllib import parse


class Box:
    """A Jahia Box. Can be of type text, infoscience, etc."""

    # WP box types
    TYPE_TEXT = "text"
    TYPE_COLORED_TEXT = "coloredText"
    TYPE_INFOSCIENCE = "infoscience"
    TYPE_ACTU = "actu"
    TYPE_MEMENTO = "memento"
    TYPE_FAQ = "faq"
    TYPE_TOGGLE = "toggle"
    TYPE_INCLUDE = "include"
    TYPE_CONTACT = "contact"
    TYPE_XML = "xml"

    # Mapping of known box types from Jahia to WP
    types = {
        "epfl:textBox": TYPE_TEXT,
        "epfl:coloredTextBox": TYPE_COLORED_TEXT,
        "epfl:infoscienceBox": TYPE_INFOSCIENCE,
        "epfl:actuBox": TYPE_ACTU,
        "epfl:mementoBox": TYPE_MEMENTO,
        "epfl:faqContainer": TYPE_FAQ,
        "epfl:toggleBox": TYPE_TOGGLE,
        "epfl:htmlBox": TYPE_INCLUDE,
        "epfl:contactBox": TYPE_CONTACT,
        "epfl:xmlBox": TYPE_XML
    }

    def __init__(self, site, page_content, element, multibox=False):
        self.site = site
        self.page_content = page_content
        self.type = ""
        self.set_type(element)
        self.title = Utils.get_tag_attribute(element, "boxTitle", "jahia:value")
        self.content = ""
        self.set_content(element, multibox)

    def set_type(self, element):
        """
        Sets the box type
        """

        type = element.getAttribute("jcr:primaryType")

        if type in self.types:
            self.type = self.types[type]
        else:
            self.type = type

    def set_content(self, element, multibox=False):
        """set the box attributes"""

        # text
        if self.TYPE_TEXT == self.type or self.TYPE_COLORED_TEXT == self.type:
            self.set_box_text(element, multibox)
        # infoscience
        elif self.TYPE_INFOSCIENCE == self.type:
            self.set_box_infoscience(element)
        # actu
        elif self.TYPE_ACTU == self.type:
            self.set_box_actu(element)
        # memento
        elif self.TYPE_MEMENTO == self.type:
            self.set_box_memento(element)
        # faq
        elif self.TYPE_FAQ == self.type:
            self.set_box_faq(element)
        # toggle
        elif self.TYPE_TOGGLE == self.type:
            self.set_box_toggle(element)
        # include
        elif self.TYPE_INCLUDE == self.type:
            self.set_box_include(element)
        # contact
        elif self.TYPE_CONTACT == self.type:
            self.set_box_contact(element)
        # xml
        elif self.TYPE_XML == self.type:
            self.set_box_xml(element)
        # unknown
        else:
            self.set_box_unknown(element)

    def set_box_text(self, element, multibox=False):
        """set the attributes of a text box"""

        if not multibox:
            self.content = Utils.get_tag_attribute(element, "text", "jahia:value")
        else:
            # Concatenate HTML content of many boxes
            content = ""
            elements = element.getElementsByTagName("text")
            for element in elements:
                content += element.getAttribute("jahia:value")
            self.content = content

    @staticmethod
    def _extract_epfl_news_parameters(url):
        """
        Extract parameters form url
        """
        parameters = parse.parse_qs(parse.urlparse(url).query)

        if 'channel' in parameters:
            channel_id = parameters['channel'][0]
        else:
            channel_id = ""
            logging.error("News Shortcode - channel ID is missing")

        if 'lang' in parameters:
            lang = parameters['lang'][0]
        else:
            lang = ""
            logging.error("News Shortcode - lang is missing")

        if 'template' in parameters:
            template = parameters['template'][0]
        else:
            template = ""
            logging.error("News Shortcode - template is missing")

        category = ""
        if 'category' in parameters:
            category = parameters['category'][0]

        themes = ""
        if 'themes' in parameters:
            themes = parameters['theme']

        return channel_id, lang, template, category, themes

    def set_box_actu(self, element):
        """set the attributes of an actu box"""

        # extract parameters from the old url of webservice
        channel_id, lang, template, category, themes = self._extract_epfl_news_parameters(
            Utils.get_tag_attribute(element, "url", "jahia:value")
        )
        html_content = '[epfl_news channel="{}" lang="{}" template="{}" '.format(
            channel_id,
            lang,
            template
        )
        if category:
            html_content += 'category="{}" '.format(category)
        if themes:
            html_content += 'themes="{}" '.format(",".join(themes))
        html_content += '/]'

        self.content = html_content

    @staticmethod
    def _extract_epfl_memento_parameters(url):
        """
        Extract parameters form url
        """
        parameters = parse.parse_qs(parse.urlparse(url).query)

        if 'memento' in parameters:
            memento_name = parameters['memento'][0]
        else:
            memento_name = ""
            logging.error("Memento Shortcode - event ID is missing")

        if 'lang' in parameters:
            lang = parameters['lang'][0]
        else:
            lang = ""
            logging.error("Memento Shortcode - lang is missing")

        if 'template' in parameters:
            template = parameters['template'][0]
        else:
            template = ""
            logging.error("Memento Shortcode - template is missing")

        return memento_name, lang, template

    def set_box_memento(self, element):
        """set the attributes of a memento box"""

        # extract parameters from the old url of webservice
        memento_name, lang, template = self._extract_epfl_memento_parameters(
            Utils.get_tag_attribute(element, "url", "jahia:value")
        )
        html_content = '[epfl_memento memento="{}" lang="{}" template="{}" '.format(
            memento_name,
            lang,
            template
        )
        html_content += '/]'

        self.content = html_content

    def set_box_infoscience(self, element):
        """set the attributes of a infoscience box"""
        url = Utils.get_tag_attribute(element, "url", "jahia:value")

        self.content = "[epfl_infoscience url=%s]" % url

    def set_box_faq(self, element):
        """set the attributes of a faq box"""
        self.question = Utils.get_tag_attribute(element, "question", "jahia:value")

        self.answer = Utils.get_tag_attribute(element, "answer", "jahia:value")

        self.content = "<h2>%s</h2><p>%s</p>" % (self.question, self.answer)

    def set_box_toggle(self, element):
        """set the attributes of a toggle box"""
        self.opened = Utils.get_tag_attribute(element, "opened", "jahia:value")

        self.content = Utils.get_tag_attribute(element, "content", "jahia:value")

    def set_box_include(self, element):
        """set the attributes of an include box"""
        url = Utils.get_tag_attribute(element, "url", "jahia:value")

        self.content = "[include url=%s]" % url

    def set_box_contact(self, element):
        """set the attributes of a contact box"""
        text = Utils.get_tag_attribute(element, "text", "jahia:value")

        self.content = text

    def set_box_xml(self, element):
        """set the attributes of a xml box"""
        xml = Utils.get_tag_attribute(element, "xml", "jahia:value")
        xslt = Utils.get_tag_attribute(element, "xslt", "jahia:value")

        self.content = "[xml xml=%s xslt=%s]" % (xml, xslt)

    def set_box_unknown(self, element):
        """set the attributes of an unknown box"""
        self.content = "[%s]" % element.getAttribute("jcr:primaryType")

    def __str__(self):
        return self.type + " " + self.title
