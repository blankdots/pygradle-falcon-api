from webapp.utils.db import connect_DB
from webapp.utils.logs import app_logger


class IndexingData(object):
    """Construct Indexing job based on plugin and indexing specification."""

    @classmethod
    def create_index(cls, data, author, timestamp):
        """Create a indexing job."""
        conn = connect_DB()
        status = "Done"
        result = cls.register_index(conn, status, data, author, timestamp)
        app_logger.info('Construct indexing job based on Index Object.')
        return result

    @classmethod
    def retrieve_indexID(cls, indexID):
        """Retrieve indexing job with ID."""
        conn = connect_DB()
        result = cls.check_index_status(conn, indexID)
        app_logger.info('Retrieve indexing job with the ID: {0}'.format(indexID))
        return result

    @classmethod
    def delete_indexID(cls, indexID):
        """Delete indexing job with ID."""
        conn = connect_DB()
        cls.delete_index(conn, indexID)
        app_logger.info('Delete indexing job with the ID: {0}'.format(indexID))
        return

    @staticmethod
    def register_index(conn, status, indexing):
        """Create the indexing job."""
        db_cursor = conn.cursor()
        # Insert a row of data
        db_cursor.execute("INSERT INTO indexes VALUES (?, ?)", (status, str(indexing)))
        # Save (commit) the changes
        conn.commit()
        result = {'id': db_cursor.lastrowid, 'status': status}
        app_logger.info('Create row in the database with indexing job ID: {0}'.format(db_cursor.lastrowid))
        db_cursor.close()
        return result

    @staticmethod
    def check_index_status(conn, indexID):
        """Check the indexing job status."""
        db_cursor = conn.cursor()
        # Insert a row of data
        for row in db_cursor.execute('SELECT rowid, indexstatus FROM indexes WHERE rowid=?', (indexID, )):
            result = {'id': row[0], 'status': row[1]}
            app_logger.info('Check status in the database for indexing job ID: {0}'.format(indexID))
            break
        else:
            result = None
            app_logger.warning('Check status: There is no record for indexing job ID: {0}'.format(indexID))
        db_cursor.close()
        return result

    @staticmethod
    def delete_index(conn, indexID):
        """Detele the indexing job data."""
        db_cursor = conn.cursor()
        # Delete a row of data
        db_cursor.execute('DELETE FROM indexes WHERE rowid=?', (indexID, ))
        # Save (commit) the changes
        conn.commit()
        app_logger.info('Delete index in the database with indexing job ID: {0}'.format(indexID))
        db_cursor.close()
        return

    @staticmethod
    def update_index_status(conn, indexID, status):
        """Update the indexing job status information."""
        db_cursor = conn.cursor()
        db_cursor.execute("SELECT rowid FROM indexes WHERE rowid = ?", (indexID,))
        data = db_cursor.fetchone()
        if data is None:
            app_logger.info('There is no record for indexing job ID:'.format(indexID))
            pass
        else:
            db_cursor.execute('UPDATE indexes SET indexstatus=? WHERE rowid=?', (status, indexID))
            # Save (commit) the changes
            conn.commit()
            app_logger.info('Update status in the database for indexing job ID: {0}'.format(indexID))
        db_cursor.close()
        return
