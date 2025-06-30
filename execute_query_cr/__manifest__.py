{
    'name': 'Execute Query',
    'version': '18.0',
    'summary': 'Execute Query',
    'depends': [],
    'sequence': 35,

    'license': 'LGPL-3',
    'installable': True,

    'assets': {
        'web.assets_frontend': [
            'execute_query_cr/static/src/**/*',
        ],
        'web._assets_core': [          
            'execute_query_cr/static/src/**/*',
        ],
        'web.assets_backend':[
             'execute_query_cr/static/src/**/*',
        ]
    }
}
