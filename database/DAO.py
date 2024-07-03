from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getNodes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct g.Chromosome as Chromosome
                from genes g 
                where g.Chromosome != 0
                order by g.Chromosome asc """

        cursor.execute(query, ())

        for row in cursor:
            result.append(row['Chromosome'])
            # result.append(ArtObject(object_id=row["object_id"], ... ))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select  distinct g.Chromosome as Chromosome1, g2.Chromosome as Chromosome2
                    from interactions i , genes g, genes g2
                    where i.GeneID1 = g.GeneID and i.GeneID2 = g2.GeneID and g.Chromosome != g2.Chromosome and g.Chromosome != 0 and g2.Chromosome != 0
                    order by g.Chromosome asc, g2.Chromosome asc"""

        cursor.execute(query, ())

        for row in cursor:
            result.append((row['Chromosome1'],row['Chromosome2']))
            # result.append(ArtObject(object_id=row["object_id"], ... ))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(n1, n2):
        conn = DBConnect.get_connection()

        result = 0

        cursor = conn.cursor(dictionary=True)
        #query = """select sum( distinct i.Expression_Corr) as peso
        #            from genes g , genes g2, interactions i
        #            where i.GeneID1 = g.GeneID and i.GeneID2 = g2.GeneID and g.Chromosome = %s and g2.Chromosome = %s
        #            group by g.Chromosome, g2.Chromosome """

        query="""select sum(interazioni.Correl) as peso
                from (select distinct g.geneID as geneID1, g2.GeneID as geneID2, i.Expression_Corr as Correl
                from genes g , genes g2, interactions i
                where i.GeneID1 = g.GeneID and i.GeneID2 = g2.GeneID and g.Chromosome = %s and g2.Chromosome = %s) as interazioni"""

        cursor.execute(query, (n1, n2))

        for row in cursor:
            result = row['peso']
            # result.append(ArtObject(object_id=row["object_id"], ... ))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllPesi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query="""select Chromosome1, Chromosome2, sum(interazioni.Correl) as peso
                from (select distinct g.Chromosome as Chromosome1, g2.Chromosome as Chromosome2, g.geneID as geneID1, g2.GeneID as geneID2, i.Expression_Corr as Correl
                from genes g , genes g2, interactions i
                where i.GeneID1 = g.GeneID and i.GeneID2 = g2.GeneID and g.Chromosome != g2.Chromosome and g.Chromosome != 0 and g2.Chromosome != 0) as interazioni
                group by Chromosome1, Chromosome2"""

        cursor.execute(query, ())

        for row in cursor:
            result.append((row['Chromosome1'], row['Chromosome2'], row['peso']))
            # result.append(ArtObject(object_id=row["object_id"], ... ))

        cursor.close()
        conn.close()
        return result
