import pickle
def globalization() :
    global main_module_variable_1, main_module_variable_2
    main_module_variable_1, main_module_variable_2 = pickle.load( open( "pickled variables.p", "rb" ) )

def function_3() :
	globalization()
	return main_module_variable_1