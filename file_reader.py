with open('linguistica/datasets/vergil_aeneid.txt', 'w+') as data:
	plaintext = data.read()

plaintext = plaintext.replace(',', '')
