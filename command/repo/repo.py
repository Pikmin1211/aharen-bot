import os
from git import Repo
from discord.ext import commands

repo_cache = os.path.join(os.path.dirname(__file__), 'repo.cache')
dir_repos = os.path.join(os.path.dirname(__file__), 'repos\\')

def get_dir_repos():
	return dir_repos

def get_working_repo():
	if (os.path.isfile(repo_cache)):
		cache = open(repo_cache, 'r')
		working_repo = cache.readline()
		cache.close()
		return working_repo
	else:
		raise Exception('There is no working repo!')

def set_working_repo(repo: str):
	cache = open(repo_cache, 'w')
	cache.write(repo)
	cache.close()

def get_repos(path: str = None):
	if (path is None):
		path = get_dir_repos()
	repos = []
	for directory in os.listdir(path):
		directory = os.path.join(get_dir_repos(), directory)
		if (os.path.isdir(os.path.join(directory, '.git\\'))):
			rp = [os.path.basename(os.path.normpath(directory)), Repo(os.path.join(get_dir_repos(), directory)), os.path.join(get_dir_repos(), directory)]
			repos.append(rp)
	return repos

@commands.command()
async def repo_list(ctx):
	repos = get_repos()
	if len(repos) == 0:
		await ctx.send('There are no repos!')
		return
	elif len(repos) == 1:
		await ctx.send('I found 1 repo!')
	else:
		await ctx.send('I found {0} repos!'.format(len(repos)))
	response = '```\n'
	for rp in repos:
		response += '{0}\n'.format(rp[0])
	response += '```'
	await ctx.send(response)

@commands.command()
async def repo_set(ctx, name: str):
	set_working_repo(name)
	await ctx.send('I have set {0} as the working repo.'.format(name))

def setup(aharen):
	aharen.add_command(repo_list)
	aharen.add_command(repo_set)
