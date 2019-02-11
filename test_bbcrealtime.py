# encoding: utf-8
import unittest

import bbcrealtime


class TestBbcRealtime(unittest.TestCase):
    def test_something(self):
        # Arrange
        stations = ["bbc6music", "bbcradio1", "bbcradio2", "bbc1xtra"]

        for station in stations:
            # Hopefully at least one station is currently playing something
            # and not returning None

            # Act
            realtime = bbcrealtime.nowplaying(station)

            if realtime is not None:
                break

        # Assert
        self.assertIsNotNone(realtime)
        self.assertIn("start", realtime)
        self.assertIn("end", realtime)
        self.assertGreater(realtime["end"], 1_520_157_840)
        self.assertGreater(realtime["end"], realtime["start"])


if __name__ == "__main__":
    unittest.main()

# End of  file
