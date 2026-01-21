"""
Core framework module.

Contains the foundational classes for the test automation framework:
- BasePage: Abstract base class for all page objects
- ElementHandler: Wrapper for element interactions
"""

from core.base_page import BasePage
from core.element_handler import ElementHandler

__all__ = ["BasePage", "ElementHandler"]