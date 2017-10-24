import re

from collections import deque
from checks import AgentCheck

class LogsCheck(AgentCheck):
	def check(self, instance):
		
		#Load values from the instance config
		logs = instance['logs']
		default_lines_check = self.init_config.get('default_lines_check', 100)
		lines_check = float(instance.get('lines_check', default_lines_check))
		default_regex = self.init_config.get('default_regex', 'error')
		regex = str(instance.get('regex', default_regex))
		default_metric_name = self.init_config.get('default_metric_name', 'mml.logs.error_counter')
		metric_name = str(instance.get('metric_name', default_metric_name))
		default_tag = self.init_config.get('default_tag', [])
		tag = instance.get('tag', default_tag)

		#Get count result
		count_list =[]
		with open(logs) as file:
			for line in deque(file, lines_check):
				x = re.search(regex, line, re.IGNORECASE)
				if x != None:
	  				count_list.append(x.group(0))
		count = len(count_list)
		self.gauge(metric_name, count, tags=tag)

if __name__ == '__main__':
    check.check(instance)