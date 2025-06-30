from snake.game import Game, GameConf, GameMode

DQN_SOLVER = "DQNSolver" 

MODE = GameMode.TRAIN_DQN_GUI 

conf = GameConf()
conf.solver_name = DQN_SOLVER
conf.mode = MODE


print("\n=== Snake RL Research Experiment ===")
print(f"Solver: {conf.solver_name}")
print(f"Mode: {conf.mode}")
print(f"Map size: {conf.map_rows}x{conf.map_cols}")
print("====================================\n")

Game(conf).run()

from snake.solver.base import SolverBase

class PPOAgent(SolverBase):
    def __init__(self, ...):
        super().__init__(...)
       

    def select_action(self, state):
        pass

    def train(self, ...):
        # PPO training loop
        pass
