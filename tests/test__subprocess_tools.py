#!/usr/bin/env python3
"""Unit test cases for testing the subprocess tools and subproces sutilities of impsia_python_toolbox."""

import unittest
import logging
import subprocess
from logging import Logger
from typing import Any
from src.impsia.python_toolbox.subprocess_tools import SubprocessRunner    # pylint: disable=import-error
from src.impsia.python_toolbox.subprocess_tools import KEY_SUCCESSFUL_PROCESS, KEY_FAILED_PROCESS, KEY_TIMEOUT_PROCESS  # pylint: disable=import-error
########################################
# The above import statement is fine by most linters except for pylint, which throws the following error:
# E0401: Unable to import 'src.impsia.python_toolbox.subprocess_tools' (import-error)
#
# The following import construct is a possible workaround for pylint--error:
# import sys
# sys.path.append('src/')
# from impsia.python_toolbox.subprocess_tools import SubprocessRunner
#
# But this import-construct raises more problems.
# - it's not supported by mypy (import-not-found)
# - it causes another positioning-error in pylint and flake8 (because of the sys.path.append()-statement):
# pylint C0413: Import "from impsia.p... import SubprocessRunner" should be placed at the top of the module (wrong-import-position)
# flake8 E402 module level import not at top of file
########################################
_LOGGER: Logger = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)

__all__: list[str] = ['TestSubprocessRunner']


class TestSubprocessRunner(unittest.TestCase):
	"""Test SubprocessRunner-wrapper."""
	def test_run_commandline__echo(self) -> None:
		"""Test SubprocessRunner.run_commandline with simple echo-command."""
		echo_text: str = 'gotcha! echo was successful!'
		runner: SubprocessRunner = SubprocessRunner()
		commandline_args = ['echo', f'"{echo_text}"']
		results: dict[str, Any] = runner.run_commandline(commandline_args, suppress_missing_timeout_warning=False)
		self.assertIsNone(results[KEY_TIMEOUT_PROCESS], 'The executed subprocess ran into a timeout unexpectedly.')
		self.assertIsNone(results[KEY_FAILED_PROCESS], 'The executed subprocess failed unexpectedly.')
		process_data: subprocess.CompletedProcess = results[KEY_SUCCESSFUL_PROCESS]
		self.assertIsNotNone(process_data, 'The executed subprocess yielded output None instead of the expected process-object.')
		self.assertIsInstance(process_data, subprocess.CompletedProcess, 'The executed subprocess didn\'t yield a process-object as expected.')
		stdout_value: str = process_data.stdout
		stdout_value = stdout_value.strip().strip('"')
		self.assertEqual(stdout_value, echo_text,
			'The stdout-result from the executed subprocess is not as expected because it doesn\'t contain the expected keywords.')

	def test_run_commandline__timeout(self) -> None:
		"""Test SubprocessRunner.run_commandline with hanging cat-command and force timeout."""
		runner: SubprocessRunner = SubprocessRunner()
		test_timeout_seconds = 1
		commandline_args = ['cat', '-']
		results: dict[str, Any] = runner.run_commandline(commandline_args, timeout=test_timeout_seconds)
		self.assertIsNone(results[KEY_SUCCESSFUL_PROCESS], 'The executed subprocess unexpectedly finished successful without timeout.')
		self.assertIsNone(results[KEY_FAILED_PROCESS], 'The executed subprocess failed unexpectedly.')
		timeout_data: subprocess.TimeoutExpired = results[KEY_TIMEOUT_PROCESS]
		self.assertIsNotNone(timeout_data, 'The executed subprocess yielded output None instead of the expected timeout-object.')
		self.assertIsInstance(timeout_data, subprocess.TimeoutExpired, 'The executed subprocess didn\'t yield a timeout-object as expected.')
		self.assertEqual(timeout_data.timeout, test_timeout_seconds, 'The resulting timeout-object contains different value for timeout duration.')
		self.assertEqual(timeout_data.cmd, commandline_args, 'The resulting timeout-object contains different commandline arguments.')
		_LOGGER.info(f'timeout info: {timeout_data}')

	def test_run_commandline__error(self) -> None:
		"""Test SubprocessRunner.run_commandline with crashing cat-command and force error."""
		runner: SubprocessRunner = SubprocessRunner()
		commandline_args = ['cat', 'nonExistingFileForTest001.txt']
		results: dict[str, Any] = runner.run_commandline(commandline_args, suppress_missing_timeout_warning=True)
		self.assertIsNone(results[KEY_SUCCESSFUL_PROCESS], 'The executed subprocess unexpectedly finished successful without error.')
		self.assertIsNone(results[KEY_TIMEOUT_PROCESS], 'The executed subprocess ran into a timeout unexpectedly.')
		error_data: subprocess.CalledProcessError = results[KEY_FAILED_PROCESS]
		self.assertIsNotNone(error_data, 'The executed subprocess yielded output None instead of the expected error-object.')
		self.assertIsInstance(error_data, subprocess.CalledProcessError, 'The executed subprocess didn\'t yield a error-object as expected.')
		self.assertEqual(error_data.returncode, 1, 'The resulting error-object contains unexpected return code.')
		self.assertEqual(error_data.cmd, commandline_args, 'The resulting error-object contains different commandline arguments.')
		_LOGGER.info(f'error info: {error_data}')


if __name__ == '__main__':
	unittest.main()
