# main.py
import multiprocessing as mp
from eeg_sim import simulator_process
from eeg_game import game_process
from plot_qt import plot_process

def main():
    mp.set_start_method("spawn", force=True)

    sample_q = mp.Queue(maxsize=8000)

    # IMPORTANT: two separate event queues
    event_q_game = mp.Queue(maxsize=200)
    event_q_plot = mp.Queue(maxsize=200)

    control_q = mp.Queue(maxsize=50)

    sim_p  = mp.Process(target=simulator_process, args=(sample_q, event_q_game, event_q_plot, control_q))
    game_p = mp.Process(target=game_process, args=(event_q_game, control_q))
    plot_p = mp.Process(target=plot_process, args=(sample_q, event_q_plot))

    sim_p.start()
    game_p.start()
    plot_p.start()

    game_p.join()

    # Cleanup
    for p in (sim_p, plot_p):
        if p.is_alive():
            p.terminate()

if __name__ == "__main__":
    main()
