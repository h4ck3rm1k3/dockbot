def get_db_url(config):
    backend = config.database.get('backend', 'sqlite3')
    if backend == 'sqlite3':
        return 'sqlite:///{0}'.format(config.database.get('name'))
    if backend == 'postgres':
        base_url = 'postgresql://{user}:{password}@localhost:{port}/{db_name}'
        return base_url.format(
            user=config.database['user'],
            password=config.database['password'],
            db_name=config.database.get('name'),
            port=config.database.get('port', 5432),
        )
