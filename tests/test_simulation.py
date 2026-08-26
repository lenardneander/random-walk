import os
import tempfile
import unittest
import numpy as np
import pandas as pd

from random_walk.boundaries import Boundary, BoundaryType
from random_walk.walker import Walker
from random_walk.simulation import Simulation, NeighborhoodType

class TestRandomWalk(unittest.TestCase):
    def test_walker_creation_and_trajectory(self):
        w = Walker(walker_id=1, initial_position=[0.0, 0.0], speed=2.0)
        self.assertEqual(w.dimension, 2)
        self.assertEqual(len(w.history), 1)
        w.record_position([2.0, 0.0])
        self.assertEqual(len(w.history), 2)
        self.assertTrue(np.array_equal(w.position, [2.0, 0.0]))

    def test_step_set_generation_2d(self):
        sim_vn = Simulation(dimension=2, neighborhood_type=NeighborhoodType.VON_NEUMANN)
        self.assertEqual(len(sim_vn.step_set), 4)

        sim_moore = Simulation(dimension=2, neighborhood_type=NeighborhoodType.MOORE)
        self.assertEqual(len(sim_moore.step_set), 8)

    def test_step_set_generation_3d(self):
        sim_vn = Simulation(dimension=3, neighborhood_type=NeighborhoodType.VON_NEUMANN)
        self.assertEqual(len(sim_vn.step_set), 6)

        sim_moore = Simulation(dimension=3, neighborhood_type=NeighborhoodType.MOORE)
        self.assertEqual(len(sim_moore.step_set), 26)

    def test_reflective_boundary(self):
        bnd = Boundary(dimension=2, boundary_type=BoundaryType.REFLECTIVE, limits=[(-5.0, 5.0), (-5.0, 5.0)])
        current_pos = np.array([4.0, 0.0])
        step_vec = np.array([3.0, 0.0])  # Proposed pos: 7.0
        new_pos, is_active = bnd.process_step(current_pos, step_vec)
        # Overshoot by 2.0 past 5.0 -> reflects back to 3.0
        self.assertTrue(is_active)
        self.assertAlmostEqual(new_pos[0], 3.0)
        self.assertAlmostEqual(new_pos[1], 0.0)

    def test_absorbing_boundary(self):
        bnd = Boundary(dimension=2, boundary_type=BoundaryType.ABSORBING, limits=[(-5.0, 5.0), (-5.0, 5.0)])
        current_pos = np.array([4.0, 0.0])
        step_vec = np.array([3.0, 0.0])  # Proposed pos: 7.0
        new_pos, is_active = bnd.process_step(current_pos, step_vec)
        self.assertFalse(is_active)
        self.assertEqual(new_pos[0], 5.0)

    def test_simulation_run_and_dataframe(self):
        sim = Simulation(dimension=3, neighborhood_type=NeighborhoodType.MOORE, seed=42)
        sim.create_walkers(num_walkers=3)
        sim.run(num_steps=10)
        
        df = sim.to_dataframe()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3 * 11)  # 11 trajectory points per walker
        self.assertIn('z', df.columns)

    def test_csv_export(self):
        sim = Simulation(dimension=2, seed=123)
        sim.create_walkers(num_walkers=2)
        sim.run(num_steps=5)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, 'test_out.csv')
            sim.save_csv(csv_path)
            self.assertTrue(os.path.exists(csv_path))
            loaded_df = pd.read_csv(csv_path)
            self.assertEqual(len(loaded_df), 2 * 6)

if __name__ == '__main__':
    unittest.main()
