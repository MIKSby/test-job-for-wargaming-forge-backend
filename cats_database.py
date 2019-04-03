import psycopg2


class CatsDatabase:
    def __init__(self, auth):
        self.auth = auth

    def execute(self, sql, data=None, get=None):
        with psycopg2.connect(dsn=self.auth) as conn:
            with conn.cursor() as curs:
                curs.execute(sql, data)
                return curs.fetchall() if get else None

    def get_cats(self):
        return self.execute('SELECT * FROM public.cats;', get=True)
