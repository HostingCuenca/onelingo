import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "contenido"))

from importar_biblioteca import canonical, sha256, slug  # noqa: E402


class ImportLibraryTest(unittest.TestCase):
    def test_canonical_hash_ignores_mapping_order(self):
        self.assertEqual(sha256({"b": 2, "a": 1}), sha256({"a": 1, "b": 2}))

    def test_slug_is_stable_and_position_independent(self):
        self.assertEqual("unit.item-a", slug("Unit.Item_A"))
        self.assertEqual(canonical({"b": 2, "a": 1}), '{"a":1,"b":2}')


if __name__ == "__main__":
    unittest.main()
