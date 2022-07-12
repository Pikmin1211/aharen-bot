import os
import json
from ..repo import repo
from git import Repo
from discord.ext import commands

default_message = 'Automated commit.'
config_file = open(os.path.join(os.getcwd(), 'config.json'))
config = json.load(config_file)
config_file.close()

@commands.command()
async def git_clone(ctx, url: str, branch: str = 'master'):
	await ctx.send('Working on it... please be patient.')
	name = url.split('/')[-1]
	url = 'https://{0}:{1}@{2}.git'.format(config['github-username'], config['github-token'], url.replace('https://', ''))
	Repo.clone_from(url, os.path.join(repo.get_dir_repos(), name), branch=branch)
	new_repo = Repo(os.path.join(repo.get_dir_repos(), name))
	with new_repo.config_writer() as cw:
		cw.set_value('user', 'name', config['github-username'])
		cw.set_value('user', 'email', config['github-email'])
		cw.release()
	await ctx.send('I have cloned the repo!')

@commands.command()
async def git_commit(ctx, message: str = default_message, name: str = '', file: str = '*'):
	if name == '':
		name = repo.get_working_repo()
	else:
		repo.set_working_repo(name)
	for rp in get_repos():
		if rp[0].lower() == name.lower():
			rp[1].git.add(file)
			rp[1].git.commit(m=message)
			await ctx.send('I have made the commit!')

@commands.command()
async def git_push(ctx, name: str = ''):
	if name == '':
		name = repo.get_working_repo()
	else:
		repo.set_working_repo(name)
	for rp in repo.get_repos():
		if rp[0].lower() == name.lower():
			origin = rp[1].remote('origin')
			origin.push()
			await ctx.send('I have made the push!')

@commands.command()
async def git_commit_push(ctx, message = default_message, name: str = ''):
	await git_commit(ctx, message, name)
	await git_push(ctx, name)

def setup(aharen):
	aharen.add_command(git_clone)
	aharen.add_command(git_commit)
	aharen.add_command(git_push)
	aharen.add_command(git_commit_push)
