espNetConfig
============

ESP-32 Network Config.  If ST mode fails, enable AP mode to configure ST.::

  import esp32_net_config
  esp32_net_config.connect_network_or_go_into_config_mode()
