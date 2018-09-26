# qhalignedlayout
Multiple QHAlignedLayouts can be set on separate widgets, and grouped together to remain aligned with one another.

See test_qhalignedlayout.py for example usage.

QHAlignedLayout behaves like a QHBoxLayout, but will keep itself aligned with all of the other QHAlignedLayouts in its group.

You create QHAlignedLayoutGroup, then pass that object to the construtor of each of the QHAlignedLayout objects you want to
keep aligned with one another.

getGeometry, sizeHint and minimumSize have all been overriden.
