import os
import requests
from discord.ext import commands

dir_clib = os.path.join(os.path.dirname(__file__), 'FE-CLib\\')
dir_gbafe = os.path.join(dir_clib, 'include\\gbafe\\')
dir_ref = os.path.join(dir_clib, 'reference\\FE8U-20190316.s')

def make_response_list(results: list[str], language: str = 'c'):
	response_list = []
	response = '```{0}\n'.format(language)

	for result in results:
		if len(response + result) + 10 < 2000:
			response += result
		else:
			response += '```'
			response_list.append(response)
			response = '```{0}\n'.format(language)
			response += result

	response += '```'
	response_list.append(response)
	return response_list

async def respond_with_list(ctx, results: list[str], language: str = 'c'):
	if len(results) == 0:
		await ctx.send('Sorry, but no results were found.')
		return
	elif len(results) == 1:
		await ctx.send('I found 1 result!\n')
	else:
		await ctx.send('I found {0} results!\n'.format(len(results)))

	for response in make_response_list(results, language):
		await ctx.send(response)

@commands.command()
async def clib_ref_search(ctx, term: str):
	results = []
	
	with open(dir_ref, 'r', encoding = 'utf-8') as rfile:
		for line in rfile.readlines():
			if len(line.split(' ')) == 3:
				if term.lower() in line.split(' ')[1].lower():
					results.append(line)
		rfile.close()

	await respond_with_list(ctx, results, 'arm')

def get_dir_clib_struct(term: str):
	result = ''
	reading = False
	for root, dirs, files in os.walk(dir_gbafe):
		for file in files:
			if file.endswith('.h'):
				with open(os.path.join(root, file), 'r', encoding = 'utf-8') as hfile:
					for line in hfile.readlines():
						if 'struct {0} {{'.format(term.lower()) in line.lower():
							reading = True
						if reading:
							result += line
						if '}' in line and reading:
							hfile.close()
							return result
					hfile.close()
	return result

@commands.command()
async def clib_struct_search(ctx, term: str):
	result = get_dir_clib_struct(term)

	if result == '':
		await ctx.send('Sorry, but no results were found.')
		return

	await ctx.send('I found the following struct!\n```c\n{0}```'.format(result))

def try_detect_function(line: str):
	if ';' in line and 'extern' not in line and 'FE8U' in line:
		return True

	return False

def try_get_function_name(line: str):
	name = ''

	for char in line:
		if char == '(':
			return name
		name += char
		if char == ' ':
			name = ''

	return name

@commands.command()
async def clib_func_search(ctx, term: str):
	results = []

	for root, dirs, files in os.walk(dir_gbafe):
		for file in files:
			if file.endswith('.h'):
				with open(os.path.join(root, file), 'r', encoding = 'utf-8') as hfile:
					for line in hfile.readlines():
						if try_detect_function(line) and term.lower() in try_get_function_name(line.lower()):
							results.append(line)
					hfile.close()

	await respond_with_list(ctx, results)

def setup(aharen):
	aharen.add_command(clib_struct_search)
	aharen.add_command(clib_ref_search)
	aharen.add_command(clib_func_search)
