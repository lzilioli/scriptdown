import sys
import re

regex = {
	'single-comment': '\/\/.*',
	'block-comment' : '\/\*.*\*\/'
}

## Open the file
f = open(sys.argv[1], 'r').read()
f = re.sub(regex['single-comment'], '', f)
f = re.sub(regex['block-comment'], '', f, flags=re.DOTALL)
contents = f.splitlines()

blankLineCount = 0
state = 'meta'
meta = {}
output = ''

for line in contents:
	if state == 'meta':
		# If the line is blank
		if not line.strip():
			blankLineCount += 1
			# After two blank lines, we presume the meta section is done
			if blankLineCount == 2:
				# Switch to script state
				state = 'script'
				# Add the title to the output
				output += '\
				<div class="title">\
					<div class="show">' + meta['show'] + '</div>\
					<div class="episode">"' + meta['episode'] + '"</div>\
					<div class="author">written by<br>' + meta['author'] + '</div>\
				</div>'
		else:
			blankLineCount = 0
			lineWords = line.split(' ')
			key = lineWords[0]
			meta[key] = line.replace(key, ' ').strip()
	if state == 'script':
		trimmedLine = line.strip();
		if line and line[0] == '\t':
			output += '<p class="parenthetical">(' + line.strip() + ')</p>\n'
		elif trimmedLine:
			if trimmedLine[:2] == '/#':
				trimmedLine = trimmedLine.replace('/#', '', 1).strip()
				output += '<p class="scene-end">End ' + trimmedLine + '</p>\n'
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

output = """
	<div id="header">
		<div class="show">%s</div>
		<div class="episode">%s</div>
		<div class="date">%s</div>
		<div class="note">%s</div>
	</div>
	<div id="content">
		""" + output + """
	</div>
	<div id="footer"></div>
"""

output %= (meta['show'], meta['episode'], meta['date'], meta['note'])

print(output.strip())
