import os
from shellpilot.decorators import log_action

class BashHistory:
    def __init__(commands :list[str]):
        self.command = commands