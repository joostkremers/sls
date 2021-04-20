"""A kivy layout with a set number of rows and columns, whose children are
positioned according to their `column` and `row` properties if they exist. If
they do not have these properties, they default to the zeroth column and row.

Grid items can span more than one position on the grid by passing a `span`
argument, which defaults to (1, 1). Setting it to e.g., (1, 2) results in an
item that spans two rows.

"""

# Adapted from https://github.com/inclement/sparsegridlayout/

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.event import EventDispatcher


class SparseGridLayout(FloatLayout):

    rows = NumericProperty(1)
    columns = NumericProperty(1)
    # shape = ReferenceListProperty(columns, rows)

    def do_layout(self, *args):
        shape_hint = (1 / self.columns, 1 / self.rows)
        for child in self.children:
            child.size_hint = (
                shape_hint[0] * child.span[0],
                shape_hint[1] * child.span[1],
            )
            if not hasattr(child, "row"):
                child.row = 0
            if not hasattr(child, "column"):
                child.column = 0

            child.pos_hint = {
                "x": shape_hint[0] * child.column,
                "y": shape_hint[1] * child.row,
            }
        super(SparseGridLayout, self).do_layout(*args)


class SparseGridEntry(EventDispatcher):
    row = NumericProperty(0)
    column = NumericProperty(0)
    span_x = NumericProperty(1)
    span_y = NumericProperty(1)
    span = ReferenceListProperty(span_x, span_y)
