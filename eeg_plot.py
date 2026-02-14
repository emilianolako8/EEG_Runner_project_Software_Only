# eeg_plot.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def run_plot(shared, stop_flag):
    """
    Runs the EEG plot window.
    This should run in the MAIN thread on some systems.
    (But often works in a thread too. We'll run it in main to be safe.)

    We read shared samples and redraw the line.
    """
    fig, ax = plt.subplots()
    ax.set_title("Simulated EEG (real-time)")
    ax.set_xlabel("Samples (latest on right)")
    ax.set_ylabel("Amplitude")

    line, = ax.plot([], [], lw=1)

    # visual blink marker text
    blink_text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    def init():
        ax.set_xlim(0, 512)
        ax.set_ylim(-120, 260)  # adjust if you change spike strength
        line.set_data([], [])
        return line, blink_text

    def update(_frame):
        if stop_flag["stop"]:
            plt.close(fig)
            return line, blink_text

        y = shared.get_samples_copy()
        if not y:
            return line, blink_text

        # keep last 512 samples for plotting
        y = y[-512:]
        x = list(range(len(y)))
        line.set_data(x, y)

        # show blink indicator if event exists (we do NOT consume it here)
        # (consuming happens in the game)
        blink_text.set_text("")

        return line, blink_text

    ani = animation.FuncAnimation(
        fig, update, init_func=init,
        interval=30, blit=False
    )
    plt.show()
