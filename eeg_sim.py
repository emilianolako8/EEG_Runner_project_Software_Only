import time
import math
import random

def simulator_process(sample_q, event_q_game, event_q_plot, control_q, fs=256):
    dt = 1.0 / fs
    t = 0.0

    alpha_amp = 18.0
    alpha_target = 18.0
    time_to_new_target = 0.0

    blink_samples_left = 0
    blink_total_samples = int(0.12 * fs)

    next_time = time.perf_counter()

    while True:
        # Read control messages
        try:
            while True:
                msg = control_q.get_nowait()
                if msg == "STOP":
                    return
                if msg == "BLINK":
                    blink_samples_left = blink_total_samples
                    event_q_game.put_nowait("BLINK")
                    event_q_plot.put_nowait("BLINK")
        except:
            pass

        # Change alpha slowly
        if time_to_new_target <= 0.0:
            alpha_target = random.uniform(8.0, 40.0)
            time_to_new_target = random.uniform(2.0, 4.0)

        alpha_amp += (alpha_target - alpha_amp) * 0.005
        time_to_new_target -= dt

        alpha = alpha_amp * math.sin(2 * math.pi * 10.0 * t)
        theta = 6.0 * math.sin(2 * math.pi * 6.0 * t)
        beta  = 3.0 * math.sin(2 * math.pi * 18.0 * t)
        drift = 10.0 * math.sin(2 * math.pi * 0.15 * t)
        noise = random.gauss(0.0, 6.0)

        x = alpha + theta + beta + drift + noise

        if blink_samples_left > 0:
            x += 220.0 * (blink_samples_left / blink_total_samples)
            blink_samples_left -= 1

        try:
            sample_q.put_nowait(x)
        except:
            pass

        t += dt
        next_time += dt
        sleep_for = next_time - time.perf_counter()
        if sleep_for > 0:
            time.sleep(sleep_for)
