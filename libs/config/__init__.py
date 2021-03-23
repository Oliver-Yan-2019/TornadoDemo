from configparser import ConfigParser


class Config(object):
    def __init__(self):
        self.parser = ConfigParser()

    def initialize(self, filename: str):
        """初始化

        Args:
            filename: 配置文件名

        Returns:

        """

        self.parser.read(filename, 'utf-8')

    def get_conf(self, section: str, option: str, conf_type: any = str, fallback: any = None):
        """根据section和key获取配置项

        Args:
            section: 节
            option: 键
            conf_type: 配置项类型
            fallback: 默认配置

        Returns:

        """

        if conf_type == int:
            return self.parser.getint(section, option, fallback=fallback)
        elif conf_type == bool:
            return self.parser.getboolean(section, option, fallback=fallback)
        elif conf_type == float:
            return self.parser.getfloat(section, option, fallback=fallback)
        else:
            return self.parser.get(section, option, fallback=fallback)


__all__ = [
    'Config'
]

if __name__ == '__main__':
    config = Config()
    config.initialize('./test.conf')
    print(config.get_conf('section', 'key', fallback='1'))
    print(config.get_conf('section', 'key-1', fallback='1'))
