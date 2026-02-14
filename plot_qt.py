# plot_qt.py
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
from collections import deque

def plot_process(sample_q, event_q_plot):
    app = QtWidgets.QApplication([])

    win = pg.GraphicsLayoutWidget(title="Simulated EEG (PyQtGraph)")
    win.resize(900, 400)

    plot = win.addPlot(row=0, col=0)
    plot.setYRange(-120, 280)
    curve = plot.plot()

    blink_label = pg.LabelItem(justify="left")
    win.addItem(blink_label, row=1, col=0)

    buf = deque(maxlen=512)
    blink_timer = 0

    def tick():
        nonlocal blink_timer

        # Get samples
        got_any = False
        try:
            while True:
                x = sample_q.get_nowait()
                buf.append(x)
                got_any = True
        except Exception:
            pass

        # Get blink events
        try:
            while True:
                msg = event_q_plot.get_nowait()
                if msg == "BLINK":
                    blink_timer = 15
        except Exception:
            pass

        if got_any:
            curve.setData(list(buf))

        if blink_timer > 0:
            blink_label.setText("<b style='color:yellow'>BLINK</b>")
            blink_timer -= 1
        else:
            blink_label.setText("")

    timer = QtCore.QTimer()
    timer.timeout.connect(tick)
    timer.start(30)

    win.show()
    app.exec()
