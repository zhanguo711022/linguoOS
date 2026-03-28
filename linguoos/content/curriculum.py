from dataclasses import dataclass


@dataclass
class Module:
    module_id: str
    title: str
    description: str


MODULES = [
    Module(module_id="grammar", title="Core Grammar", description="Tenses, agreement, and sentence form."),
    Module(module_id="vocabulary", title="Active Vocabulary", description="Build usable words and phrases."),
    Module(module_id="listening", title="Listening", description="Interpret common spoken patterns."),
]
