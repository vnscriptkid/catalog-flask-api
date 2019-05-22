from flask_sqlalchemy import get_debug_queries


def sql_debug(response):
    queries = list(get_debug_queries())
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration
        query = q.statement.replace('?', '{}')
        param_list = list(q.parameters)
        print(query.format(*param_list))

    print('=' * 80)
    print(' SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
    print('=' * 80)
    return response
