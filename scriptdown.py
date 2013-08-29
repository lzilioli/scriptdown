import sys
import re

regex = {
	'single-comment': '\/\/.*',
	'block-comment' : '\/\*.*\*\/'
}

f = open(sys.argv[1], 'r').read()
f = re.sub(regex['single-comment'], '', f)
f = re.sub(regex['block-comment'], '', f, flags=re.DOTALL)
contents = f.splitlines()

blankLineCount = 0
state = 'meta'
meta = {}
output = """
	<div id="header">
		<div class="show">%s</div><div class="episode">%s</div><div class="date">%s</div>
		<div class="note">%s</div>
	</div>
	<div id="content">
"""

for line in contents:
	if state == 'meta':
		if not line.strip(): # Blank line, after 2, the state changes
			blankLineCount+=1
			if blankLineCount == 2:
				output += '\
				<div class="title">\
					<div class="show">' + meta['show'] + '</div>\
					<div class="episode">' + meta['episode'] + '</div>\
					<div class="author">' + meta['author'] + '</div>\
				</div>'
				state = 'script'
		else:
			blankLineCount = 0
			lineWords = line.split(' ')
			title = lineWords[0]
			meta[title] = line.replace(title, ' ').strip()
	if state == 'script':
		trimmedLine = line.strip();
		if line and line[0] == '\t':
			output += '<p class="parenthetical">' + line.strip() + '</p>\n'
		elif trimmedLine:
			if trimmedLine[:2] == '/#':
				trimmedLine = trimmedLine.replace('/#', '', 1).strip()
				output += '<p class="scene-end">' + trimmedLine + '</p>\n'
			elif trimmedLine[0] == '>':
				trimmedLine = trimmedLine.replace('>', '')
				if(trimmedLine.endswith('..')):
					trimmedLine = trimmedLine.replace('..', ' (cont\'d.)')
				output += '<p class="name">' + trimmedLine + '</p>\n'
			elif trimmedLine[0] == '#':
				if trimmedLine[:3] == '###':
					trimmedLine = trimmedLine.replace('###', '', 1).strip()
					output += '<p class="action">' + trimmedLine + '</p>\n'
				elif trimmedLine[:2] == '##':
					trimmedLine = trimmedLine.replace('##', '', 1).strip()
					output += '<p class="loc-head">' + trimmedLine + '</p>\n'
				elif trimmedLine[:1] == '#':
					trimmedLine = trimmedLine.replace('#', '', 1).strip()
					output += '<p class="scene-head">' + trimmedLine + '</p>\n'
			else:
				output += '<p class="dialog">' + trimmedLine + '</p>\n'

output += """
	</div>
	<div id="footer">
	</div>
"""

# TODO: put on a queue the whole time and pop them off here so the order is preserved
output %= (meta['show'], meta['episode'], meta['date'], meta['note'])
print(output.strip())
