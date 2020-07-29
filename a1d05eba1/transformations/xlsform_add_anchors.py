'''
xlsform_add_anchors:

iterate through survey and choices to ensure all questions have a valid
"$anchor". These anchors are relied on throughout the code and must be unique
'''

from .transformer import Transformer
from ..utils.anchor_generator import anchor_generator

class EnsureAnchors(Transformer):
    def rw__each_row(self, row):
        if '$anchor' not in row:
            return row.copy(**{'$anchor': anchor_generator()})

    def rw__each_choice(self, cx):
        if '$anchor' not in cx:
            return cx.copy(**{'$anchor': anchor_generator()})


TRANSFORMER = EnsureAnchors()
