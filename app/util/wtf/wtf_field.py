#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wtforms import SelectMultipleField, widgets

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=True)
    option_widget = widgets.CheckboxInput()
