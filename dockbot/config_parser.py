import yaml


class DockbotConfig(object):

    def __init__(self, filename):
        with open(filename) as fh:
            yaml_data = yaml.safe_load(fh)

        self.auth = yaml_data.get('auth', {})
        self.projects = yaml_data.get('projects', [])
        self.webstatus_port = yaml_data.get('webstatus_port', 8010)
        self.database = yaml_data.get('database', {})

        # used for MailNotifier
        self.from_address = yaml_data.get('from_address', None)
        self.extra_recipients = yaml_data.get('extra_recipients', [])
        self.notifier_mode = yaml_data.get('notifier_mode', [])
