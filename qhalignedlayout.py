import sys
import math

from PySide2 import QtCore, QtGui, QtWidgets

class QHAlignedLayoutGroup(QtCore.QObject):
    def __init__(self, *args, **kwargs):
        super(QHAlignedLayoutGroup, self).__init__(*args, **kwargs)
        self._layouts = []

    def add_layout(self, layout):
        self._layouts.append(layout)

    def set_geometry(self, rect):
        if self._layouts:
            # get max/mins
            max_count = max(l.count() for l in self._layouts)
            max_widths = [None] * max_count
            for i in range(max_count):
                for l in self._layouts:
                    if i < l.count():
                        l.base_set_width(rect.width())
                        width = l.itemAt(i).geometry().width()
                        if (
                            max_widths[i] is None
                            or width > max_widths[i]
                        ):
                            max_widths[i] = width

            # take first as reference
            ref_l = self._layouts[0]

            # calc available width
            marg = ref_l.contentsMargins()
            avail_width = rect.width() - (marg.left() + marg.right() + ref_l.spacing() * (max_count-1))

            # calc suggested width
            sugg_width = sum(max_widths)

            # trim the widths to lose any overflow
            overflow = sugg_width - avail_width
            if overflow > 0:
                overflow_bit = overflow / float(sum(ref_l.stretch(i) for i in range(ref_l.count())))
                for i in range(ref_l.count()):
                    stretch = ref_l.stretch(i)
                    if stretch > 0:
                        max_widths[i] -= math.ceil(stretch * overflow_bit)

            # set max widths
            for l in self._layouts:
                l.set_child_widths(max_widths)

    def _align_widths(self, layout, method):
        max_count = max(l.count() for l in self._layouts)
        max_widths = [None] * max_count
        max_heights = [None] * max_count
        for i in range(max_count):
            for l in self._layouts:
                if i < l.count():
                    size = method(l.itemAt(i))
                    if max_widths[i] is None or size.width() > max_widths[i]:
                        max_widths[i] = size.width()
                    if max_heights[i] is None or size.height() > max_heights[i]:
                        max_heights[i] = size.height()

        # take first as reference
        ref_l = self._layouts[0]

        # sum max widths with margins and spacing
        marg = ref_l.contentsMargins()
        total_width = sum(max_widths) + marg.left() + marg.right() + ref_l.spacing() * (max_count-1)
        total_height = max(max_heights) + marg.top() + marg.bottom()
        return QtCore.QSize(total_width, total_height)

    def get_size_hint(self, layout):
        return self._align_widths(layout, QtGui.QLayoutItem.sizeHint)

    def get_minimum_size(self, layout):
        return self._align_widths(layout, QtGui.QLayoutItem.minimumSize)


class QHAlignedLayout(QtWidgets.QHBoxLayout):
    def __init__(self, layout_group, *args, **kwargs):
        super(QHAlignedLayout, self).__init__(*args, **kwargs)
        self._layout_group = layout_group
        self._layout_group.add_layout(self)

    def setGeometry(self, rect):
        self.base_set_geometry(rect)
        self._layout_group.set_geometry(rect)

    def base_set_geometry(self, rect):
        super(QHAlignedLayout, self).setGeometry(rect)

    def base_set_width(self, width):
        geom = self.geometry()
        super(QHAlignedLayout, self).setGeometry(
            QtCore.QRect(
                geom.left(),
                geom.top(),
                width,
                geom.height(),
            )
        )

    def set_child_widths(self, max_widths):
        x_offset = 0
        count = min(len(max_widths), self.count())
        for i in range(count):
            item = self.itemAt(i)
            width = max_widths[i]
            geom = item.geometry()
            if x_offset or geom.width() != width:
                new_x_offset = x_offset + (width - geom.width())
                item.setGeometry(
                    QtCore.QRect(
                        geom.left() + x_offset,
                        geom.top(),
                        width,
                        geom.height(),
                    )
                )
                x_offset = new_x_offset

    def sizeHint(self):
        return self._layout_group.get_size_hint(self)

    def minimumSize(self):
        return self._layout_group.get_minimum_size(self)

