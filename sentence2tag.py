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

position_detected_keywords = []
infile = open('position_detected_keywords', 'r')
for line in infile:
	position_detected_keywords.append(line.strip('\n').strip('\r\n'))
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

position = ''
# find position in sentence. detect keyword, and posseg sentence before the keyword, using nearest n or ns as position
for keyword in position_detected_keywords:
	if keyword in sentence:
		sub_sentence = sentence[:sentence.index(keyword)]
		words = pseg.cut(sub_sentence)
		for word, tag in list(reversed(list(words))):
			word = word.encode('utf8')
			tag = tag.encode('utf8')
			if tag != 'n' and tag != 'ns':
				break
			position = word + position

print position

