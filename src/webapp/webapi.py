import falcon
import time
import json
from datetime import datetime
from webapp.utils.logs import app_logger
from webapp.schemas import load_schema
from webapp.utils.validate import validate
from webapp.applib.registerdata import IndexingData
import consul


c = consul.Consul(host='attx-sandbox', port=8500)
# Register Service
c.agent.service.register('restapi',
                         service_id='restapi_try2',
                         port=4300,
                         tags=['test2', 'graph-component'])


api_version = "0.1"


class HealthCheck(object):
    """Create HealthCheck class."""

    def on_get(self, req, resp):
        """Respond on GET request to map endpoint."""
        resp.status = falcon.HTTP_200
        app_logger.info('Finished operations on /health GET Request.')


class IndexClass(object):
    """Create Indexing class for API."""

    @validate(load_schema('index'))
    def on_post(self, req, resp, parsed):
        """Respond on GET request to index endpoint."""
        data = IndexingData()
        timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        index_args = [parsed.get('data'), parsed.get('author'), timestamp]
        response = data.create_index(*index_args)
        resp.data = json.dumps(response, indent=1, sort_keys=True)
        resp.content_type = 'application/json'
        resp.status = falcon.HTTP_202
        app_logger.info('Creating/POST new data with ID: {0}.'.format(response['id']))


class IndexingResource(object):
    """Create Indexing Resource based on ID for retrieval."""

    @validate(load_schema('idtype'))
    def on_get(self, req, resp, indexID):
        """Respond on GET request to index endpoint."""
        data = IndexingData()
        response = data.retrieve_indexID(indexID)
        if response is not None:
            resp.data = json.dumps(response, indent=1, sort_keys=True)
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            app_logger.info('GET /index the data with ID: {0}.'.format(indexID))
        else:
            raise falcon.HTTPGone()
            app_logger.warning('Indexing job with ID: {0} is gone/deleted.'.format(indexID))

    def on_delete(self, req, resp, indexID):
        """Respond on GET request to index endpoint."""
        data = IndexingData()
        data.delete_indexID(indexID)
        resp.data = json.dumps({"deletedID": indexID}, indent=1, sort_keys=True)
        resp.content_type = 'application/json'
        app_logger.info('Deleted/DELETE /index data with ID: {0}.'.format(indexID))
        resp.status = falcon.HTTP_200


do_index = IndexClass()
get_index = IndexingResource()

webapp = falcon.API()
webapp.add_route('/health', HealthCheck())
webapp.add_route('/%s/index' % (api_version), do_index)
webapp.add_route('/%s/index/{indexID}' % (api_version), get_index)
app_logger.info('App is running.')
