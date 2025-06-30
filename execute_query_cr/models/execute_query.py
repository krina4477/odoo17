import logging

_logger = logging.getLogger(__name__)
import json
from odoo import http
from odoo.http import request


class QueryExecuteController(http.Controller):

    def action_execute_code(self, code):
        cr = request.env.cr

        try:

            user = request.env.user
            if user.has_group('base.group_system'):

                cr.execute("BEGIN;") 
                cr.execute(code)

                if cr.pgresult_ptr is not None:
                    result = cr.fetchall()
                    column_names = [desc[0] for desc in cr.description]
                    formatted_result = []
                    for row in result:
                        formatted_row = dict(zip(column_names, row))
                        formatted_result.append(formatted_row)
                    
                    return {
                        'success_returnred': formatted_result,
                    }
                else:
                    rows_affected = cr.rowcount
                    if(rows_affected != -1):
                        _logger.info("Rows affected by query: %d", (rows_affected))
                        cr.execute("COMMIT;")
                        return {
                            "success_affected" : rows_affected
                        }
                    else:
                        _logger.info("Message: %d", (cr.statusmessage))
                        cr.execute("COMMIT;")
                        return {
                            "message" : cr.statusmessage
                        }
            else:
                return {'error': "Don't have Access"}


        except Exception as e:
            
            _logger.error("Error while executing SQL code: %s", str(e))
            _logger.error("SQL code: %s", code)
            
            return {'error': e}


    @http.route('/execute_query', type='json', auth='user', csrf=True)
    def route_execute_query(self, **kw):
        code = kw.get('code')
        result = self.action_execute_code(code)
        return result