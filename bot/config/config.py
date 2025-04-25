from environs import Env


class Config:
    def __init__(self, path):
        env = Env()
        env.read_env(path)
        self.bot_token = env('BOT_TOKEN')
