import sqlite3


class Item:

    def __init__(self, _id, name, price):
        self.id = _id
        self.name = name
        self.price = price

    def json(self):  # convert to dict in correct order
        return {'id': self.id, 'name': self.name, 'price': self.price}
            
    def insert(self):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        cursor = connection.cursor()
        sql = "INSERT INTO items VALUES (null, ?, ?)"
        cursor.execute(sql, (self.name, self.price))
        connection.commit()
        self.id = cursor.execute("select last_insert_rowid()").fetchone()[0]
        connection.close()
        return self

    def update(self):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        cursor = connection.cursor()
        sql = \
            "UPDATE items SET "\
            "name = ?, "\
            "price = ? "\
            "WHERE id = ?"
        cursor.execute(sql, (self.name, self.price, self.id))
        connection.commit()
        connection.close()
        return self

    def delete(self):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        cursor = connection.cursor()
        sql = \
            "DELETE FROM items "\
            "WHERE id = ?"
        cursor.execute(sql, (self.id,))
        connection.commit()
        connection.close()
        return True

    @classmethod
    def get_by_name(cls, name):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        # connection.row_factory = sqlite3.Row  # pylint: disable=no-member
        cursor = connection.cursor()
        sql = \
            "SELECT id, name, price "\
            "FROM items "\
            "WHERE name = ?"
        result = cursor.execute(sql, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return cls(*row)

    @classmethod
    def get_all(cls):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        connection.row_factory = sqlite3.Row  # pylint: disable=no-member
        cursor = connection.cursor()
        result = cursor.execute("SELECT id, name, price FROM items")
        rows = result.fetchall()
        connection.close()
        if rows:
            return [cls(*row) for row in rows]
        else:
            return None