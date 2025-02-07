#!/usr/bin/env python3
"""TODO"""

import unittest
from typing import List, Dict, Any
from impsia_python_toolbox.impsia_subprocess_handling import SubprocessRunner


class TestRunCommandline(unittest.TestCase):
	def test_run_commandline(self):
		echo_text: str = 'gotcha stdout'
		runner: SubprocessRunner = SubprocessRunner()
		results: dict[str,Any] = runner.run_commandline(f'echo "{echo_text}" ')
		stdout_value: str = results['stdout_value']
		self.assertEqual( stdout_value , echo_text, 'The stdout-result from the executed subprocess is not as expected.' )


if __name__ == '__main__':
	unittest.main()
	
