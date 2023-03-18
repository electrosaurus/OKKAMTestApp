from functools import lru_cache
from psycopg2.extensions import connection as PGConnection
from textwrap import dedent
    

class AudienceCalculator:
    ''' Calculates properties of audiences. '''

    _audience_total_weights_query_template = dedent(
        '''
        WITH
            audience AS (
                SELECT
                    date,
                    respondent_id AS id,
                    respondent_age AS age,
                    respondent_sex AS sex,
                    weight
                FROM audience
            ),
            audience_1 AS (
                SELECT id, AVG(weight) AS avg_weight
                FROM audience
                WHERE {audience_1_condition}
                GROUP BY id
            ),
            audience_2 AS (
                SELECT id, AVG(weight) AS avg_weight
                FROM audience
                WHERE {audience_2_condition}
                GROUP BY id
            )
        SELECT
            COALESCE(SUM(audience_1.avg_weight), 0),
            COALESCE(SUM(audience_2.avg_weight), 0)
        FROM audience_1 LEFT JOIN audience_2 USING (id)
        '''
    )

    def __init__(self, db_connection: PGConnection):
        '''
        Parameters
        ----------
        db_connection: `psycopg2` connection
            Connection to the Postgres database where audiences are stored.
        '''
        self._db_connection = db_connection

    @lru_cache(100)
    def calc_inclusion_percent(
        self,
        audience_1_condition: str,
        audience_2_condition: str,
    ) -> float:
        ''' 
        Calculate the percentage of inclusion of the second audience in the first, based on
        respondent's average weight.

        Parameters
        ----------
        audience_1_condition: `str`
            SQL condition to select the first audience from the database.
        audience_2_condition: `str`
            SQL condition to select the second audience from the database.

        Note
        ----
        Columns allowed in SQL conditions are:
        * `date`
        * `id` — respondent's ID
        * `age` — respondent's age
        * `sex` — responden's sex (1 — male, 2 — female)

        Returns
        -------
        `float`
            Number between 0 (audiences do not intersect) and 1 (audiences are the same).

        Raises
        ------
        `ArithmeticError`
            If audience 1 is empty or has zero weight.

        Usage example
        -------
        >>> audience_calculator.calc_inclusion_percent(
        ...     'age BETWEEN 18 AND 35',
        ...     'age > 25 AND sex = 2',
        ... )
        0.31936966814873025
        '''
        if audience_1_condition == audience_2_condition:
            return 1.0
        cursor = self._db_connection.cursor()
        query = self._audience_total_weights_query_template.format(
            audience_1_condition=audience_1_condition,
            audience_2_condition=audience_2_condition,
        )
        cursor.execute(query)
        audience_1_total_weight, audience_2_total_weight = cursor.fetchone()
        if audience_1_total_weight == 0:
            raise ArithmeticError('Audience 1 is empty or has zero weight.')
        return audience_2_total_weight / audience_1_total_weight
