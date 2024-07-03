from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_vertici():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct Chromosome as c
                    from genes g 
                    where Chromosome <> 0
                     """

        cursor.execute(query)

        for row in cursor:
            result.append(row["c"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_archi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select c as cr1, c2 as cr2, sum(Expression_Corr) as somma
                    from interactions i, (select distinct GeneID g, Chromosome c from genes g ) as gen1, 
                    (select distinct GeneID g2, Chromosome c2 from genes g2 ) as gen2
                    where gen1.g = i.GeneID1 and gen2.g2 = i.GeneID2 and c <> 0 and c2 <> 0 and c <> c2
                    group by c, c2
                    order by c, c2"""

        cursor.execute(query)

        for row in cursor:
            result.append([row["cr1"], row["cr2"], row["somma"]])

        cursor.close()
        conn.close()
        return result
