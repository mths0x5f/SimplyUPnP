def selectDevice(devices):

	for i in xrange(len(devices)):
		print 'Device ['+str(i)+'] \n\t'+ devices[i]['SERVER'] + ''
	choice = 0
	raw_input(choice)
	print devices[choice]