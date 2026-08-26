import os
import tempfile
import unittest
import numpy as np
import pandas as pd

from random_walk.walker import Walker
from random_walk.simulation import Simulation, NeighborhoodType

class TestRandomWalk(unittest.TestCase):
    def test_walker_creation_and_step(self):
        w = Walker(walker_id=1, initial_position=[0.0, 0.0], speed=2.0)
        self.assertEqual(len(w.history), 1)
        w.record_step(np.array([1.0, 0.0]))
        self.assertEqual(len(w.history), 2)
        self.assertTrue(np.array_equal(w.position, [2.0, 0.0]))

    def test_step_set_generation(self):
        sim_vn = Simulation(neighborhood_type=NeighborhoodType.VON_NEUMANN)
        self.assertEqual(len(sim_vn.step_set), 4)

        sim_moore = Simulation(neighborhood_type=NeighborhoodType.MOORE)
        self.assertEqual(len(sim_moore.step_set), 8)

    def test_simulation_run_and_dataframe(self):
        sim = Simulation(neighborhood_type=NeighborhoodType.MOORE, seed=42)
        sim.create_walkers(num_walkers=3, random_speeds=True, random_starts=True)
        sim.run(num_steps=10)

        df = sim.to_dataframe()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3 * 11)  # 11 trajectory points per walker
        self.assertListEqual(list(df.columns), ["step", "walker_id", "x", "y", "speed"])

    def test_csv_export(self):
        sim = Simulation(seed=123)
        sim.create_walkers(num_walkers=2)
        sim.run(num_steps=5)

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test_out.csv")
            sim.save_csv(csv_path)
            self.assertTrue(os.path.exists(csv_path))
            loaded_df = pd.read_csv(csv_path)
            self.assertEqual(len(loaded_df), 2 * 6)

if __name__ == "__main__":
    unittest.main()
