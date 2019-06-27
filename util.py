
def same(t1, t2):
	if type(t1) != dict or type(t2) != dict:
		if t1 == t2:
			return True, None
		else:
			return False, (t1, t2)
	diff = {}
	for k1, v1 in t1.items():
		v2 = t2.get(k1, None)
		if v2 == None:
			diff[k1] = (v1, v2)
		else:
			sa, nx = same(v1, v2)
			if not sa:
				diff[k1] = nx
	for k2, v2 in t2.items():
		v1 = t1.get(k2, None)
		if v1 == None:
			diff[k2] = (v1, v2)
	if diff:
		return False, diff
	else:
		return True, None

def prase_kv_file(f, sep='='):
	result = {}
	for line in f.split('\n'):
		key_value = line.split(sep)
		if len(key_value) == 2:
			result[key_value[0]] = key_value[1].strip('"')
	return result

