import util

def _print_diff(k, v):
	if type(v) == dict:
		for subk, subv in v.items():
			_print_diff('%s -> %s' % (k, subk), subv)
		return
	print('fact: %s\nvalue:\n\tA: %s\n\tB: %s\n' % (k, v[0], v[1]))

def print_diff(t1, t2):
	sa, diff = util.same(t1, t2)
	if sa:
		print('There is no difference on linux config between two host.')
		return
	print('linux config difference between two host:\n')
	for k, v in diff.items():
		_print_diff(k, v)