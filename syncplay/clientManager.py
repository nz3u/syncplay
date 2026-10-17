
from syncplay import ui
from syncplay.messages import getMessage
from syncplay.ui.ConfigurationGetter import ConfigurationGetter

_configurationGetter = None


class SyncplayClientManager(object):
    def run(self):
        global _configurationGetter
        _configurationGetter = ConfigurationGetter()
        config = _configurationGetter.getConfiguration()
        from syncplay.client import SyncplayClient  # Imported later, so the proper reactor is installed
        menuBar = config['menuBar'] if 'menuBar' in config else None
        graphical = not config["noGui"]
        interface = ui.getUi(graphical=graphical, passedBar=menuBar)
        syncplayClient = SyncplayClient(config["playerClass"], interface, config)
        if syncplayClient:
            # Only a UI with a start page can go back to it when connecting fails
            syncplayClient.startedFromStartPage = hasattr(interface, 'returnToStartPage')
            interface.addClient(syncplayClient)
            syncplayClient.start(config['host'], config['port'])
        else:
            interface.showErrorMessage(getMessage("unable-to-start-client-error"), True)


def prepareReconnectConfiguration(config):
    """
    Validate the configuration returned by the start page and prepare it for a
    new connection. Returns a tuple (configuration, errorMessage).
    """
    if _configurationGetter is None:
        return config, None
    return _configurationGetter.getReconnectConfiguration(config)
