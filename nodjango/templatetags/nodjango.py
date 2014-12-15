from django import template
from django.conf import settings
from django.shortcuts import render_to_response

import os
import subprocess

register = template.Library()

@register.simple_tag
def nodjango_head_scripts():
    return """
            <script src="/socket.io/socket.io.js"></script>
            <script type="text/javascript">
                var nodjango = io.connect();
            </script>
            """
