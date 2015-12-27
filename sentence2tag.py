import uniout

tags = {}
inFile = open('yelp_tags_data', 'r')
for line in inFile:
	if line[0] == '#' or line[0] == '\r' or line[0] == '\n': continue
	linearr = line.strip('\n').strip('\r\n').split(':')
	linearr[1] = linearr[1].split(',')
	if linearr[1][0] == '': linearr[1] = []
	tags.update({linearr[0]:linearr[1]})
inFile.close()

collected_tags = []

sentence = raw_input("Input a sentence: ")

for tag, keywords in tags.items():
	for keyword in keywords:
		if keyword in sentence:
			collected_tags.append(tag)
			break

print collected_tags
