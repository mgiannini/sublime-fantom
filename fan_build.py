import sublime
import sublime_plugin
import os

class FanBuildCommand(sublime_plugin.WindowCommand):
	def run(self, task='compile', **kwargs):
		self.workingDir = self._find_pod_dir()
		if not self.workingDir:
			sublime.status_message("Could not find build.fan")
			return

		if task == 'prompt':
			self.window.show_input_panel("Test", "full", self._ok, None, None)
		else:
			self.run_build(task)

	def run_build(self, task):
		execArgs = {}
		execArgs["cmd"] = ["./build.fan", task]
		execArgs["file_regex"] = "^(.*)(?:\((\\d+),(\\d+)\)|:(\\d+))"
		execArgs["working_dir"] = self.workingDir
		self.window.run_command("exec", execArgs)

	def _find_pod_dir(self):
		view = self.window.active_view()
		dir = os.path.normpath(os.path.dirname(view.file_name()))
		while True:
			if os.path.isfile(os.path.join(dir, 'build.fan')):
				return dir

			temp = os.path.normpath(os.path.dirname(dir))
			if temp == dir:
				return None

			dir = temp

	def _ok(self, task):
		self.run_build(task)
