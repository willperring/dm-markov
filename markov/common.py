def inputd( prompt, default ):

	result = input( "{0} (default='{1}'): ".format(prompt, default))
	result = default if (result == "") else result

	if str(result).upper() == "Y":
		return True
	if str(result).upper() == "N":
		return False

	return result
