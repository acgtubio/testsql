import sqlite3

class Sql:
    def __init__(self):
        self.type = ""
        self.cols = ""
        self.tableName = ""
        self.cond = ""
        self.join = ""
        self.vals = ""

    def SelectCol(self, *col):
        if self.type != "":
            raise Exception("Only one query allowed at a time.")

        if col != ():
            cols = ", ".join(col)
        else: 
            cols = "*"
        
        self.type = f"SELECT {cols} FROM"

        return self
    
    def InsertInto(self, tableName):
        if self.tableName != "":
            raise Exception("More than one table selected.")

        self.type = "INSERT INTO"
        self.tableName = tableName

        return self

    def Columns(self, *col):
        if self.cols != "":
            raise Exception("")

        if col != ():
            cols = ", ".join(col)

        self.cols = f"({cols})"

        return self

    def Delete(self, tableName):
        if self.type != "":
            raise Exception("Only one query allowed at a time.")
        
        self.type = "DELETE FROM"
        self.tableName = tableName
    
        return self

    def Values(self, vals):
        if self.vals != "":
            raise Exception("Cannot add more values.")

        self.vals = f"VALUES{vals}"

        return self

    def Table(self, tableName):
        if self.tableName != "":
            raise Exception("More than one table selected.")
        
        self.tableName = tableName

        return self
    
    def Where(self, cond):
        if self.cond != "":
            raise Exception("Cannot add more conditions.")

        self.cond = f"WHERE {cond}"

        return self

    def IJoin(self, tableName, cond):
        self.join += f"INNER JOIN {tableName} ON {cond}"

        return self

    def execute(self):
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
        command = f"{self.type} {self.tableName} {self.cols} {self.vals} {self.join} {self.cond}"

        a = c.execute(command).fetchall()
        conn.commit()
        conn.close()

        # print(f"command: {command}")
        # print(a)
        
        self.__init__()

    def createTable(self):
        conn = sqlite3.connect("test.db")
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS students(
                id VARCHAR(9),
                fname TEXT,
                mname TEXT
            );
        """)

        conn.close()


if __name__ == "__main__":
    a = Sql()
    # a.createTable()
    # a.InsertInto("students").Columns("id", "fname").Values(("2021", "Wat")).execute()
    a.SelectCol("fname").Table("students").Where("id = 2021").execute()
