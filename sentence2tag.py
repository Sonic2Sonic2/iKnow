import jieba.posseg as pseg
import uniout
import sys

tags = {}
infile = open('yelp_tags_data', 'r')
for line in infile:
	if line[0] == '#' or line[0] == '\r' or line[0] == '\n': continue
	linearr = line.strip('\n').strip('\r\n').split(':')
	linearr[1] = linearr[1].split(',')
	if linearr[1][0] == '': linearr[1] = []
	tags.update({linearr[0]:linearr[1]})
infile.close()

position_detected_keywords_front = []
position_detected_keywords_back = []
infile = open('position_detected_keywords', 'r')
while 1:
	line = infile.readline()
	if line[0] == '#' or not line: break
	position_detected_keywords_front.append(line.strip('\n').strip('\r\n'))
while 1:
	line = infile.readline()
	if not line: break
	position_detected_keywords_back.append(line.strip('\n').strip('\r\n'))
infile.close()

position_keywords = {} 
infile = open('taipeiLocationDict.txt', 'r')
for line in infile:
	if line[0] == '#' or line[0] == '\r' or line[0] == '\n': continue
	linearr = line.strip('\n').strip('\r\n').split(':')
	linearr[1] = linearr[1].split(',')
	if linearr[1][0] == '': linearr[1] = []
	position_keywords.update({linearr[0]:linearr[1]})
infile.close()

collected_tags = []

sentence = raw_input("Input a sentence: ").decode(sys.stdin.encoding).encode('utf8')

# find yelp tag in sentence
for tag, keywords in tags.items():
	for keyword in keywords:
		if keyword in sentence:
			keyword_pos = sentence.index(keyword)
			# if chinese 'no' in sentence no far before the keyword
			if '\xe4\xb8\x8d' in sentence[keyword_pos-9:keyword_pos]:
				sign = '-'
			else:
				sign = '+'
			collected_tags.append({tag:sign})
			break

print collected_tags

# find position base on keyword
position = ''
for p, keywords in position_keywords.items():
	for keyword in keywords:
		if keyword in sentence:
			position = p
			break
if position == '':
	# find position in sentence. detect keyword, and posseg sentence before the keyword, using nearest n or ns as position
	for keyword in position_detected_keywords_front:
		if keyword in sentence:
			sub_sentence = sentence[:sentence.index(keyword)]
			words = pseg.cut(sub_sentence)
			for word, tag in list(reversed(list(words))):
				word = word.encode('utf8')
				tag = tag.encode('utf8')
				print word, tag
				if tag != 'n' and tag != 'ns' and tag != 'a' and tag != 'j':
					break
				position = word + position
	if position == '':
		# from back
		for keyword in position_detected_keywords_back:
			if keyword in sentence:
				sub_sentence = sentence[sentence.index(keyword)+len(keyword):]
				words = pseg.cut(sub_sentence)
				for word, tag in list(words):
					word = word.encode('utf8')
					tag = tag.encode('utf8')
					print word, tag
					if tag != 'n' and tag != 'ns' and tag != 'a' and tag != 'j':
						break
					position = position + word

	

print position

