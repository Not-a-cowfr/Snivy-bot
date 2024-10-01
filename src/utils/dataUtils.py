import sqlite3
from typing import Optional


# Database adapter class
class UserDataAdapter:
    def __init__(self):
        """Initialize the connection to the database."""
        self.connection = sqlite3.connect("data/userData.db")
        self.create_table()

    def create_table(self):
        """Create the Users table if it doesn't exist."""
        query = '''
        CREATE TABLE IF NOT EXISTS Users (
            id BIGINT PRIMARY KEY, 
            preferred_color VARCHAR(6), 
            username VARCHAR(255), 
            minecraft_uuid CHAR(32), 
            discord_username VARCHAR(255), 
            guild VARCHAR(255)
        );
        '''
        self.connection.execute(query)
        self.connection.commit()

    def insert_user(self,
                    user_id: int,
                    preferred_color: Optional[str] = None,
                    username: Optional[str] = None,
                    minecraft_uuid: Optional[str] = None,
                    discord_username: Optional[str] = None,
                    guild: Optional[str] = None):
        query = '''
        INSERT OR REPLACE INTO Users (id, preferred_color, username, minecraft_uuid, discord_username, guild)
        VALUES (?, ?, ?, ?, ?, ?);
        '''
        self.connection.execute(query, (user_id, preferred_color, username, minecraft_uuid, discord_username, guild))
        self.connection.commit()

    def get_user(self, user_id: int):
        """Fetch a user by their ID."""
        query = 'SELECT * FROM Users WHERE id = ?;'
        cursor = self.connection.cursor()
        cursor.execute(query, (user_id,))
        return cursor.fetchone()

    def update_user(self, user_id: int,
                    preferred_color: Optional[str] = None,
                    username: Optional[str] = None,
                    minecraft_uuid: Optional[str] = None,
                    discord_username: Optional[str] = None,
                    guild: Optional[str] = None):
        if self.get_user(user_id) is None:
            self.insert_user(
                user_id=user_id
            )


        fields = []
        values = []
        if preferred_color is not None:
            fields.append("preferred_color = ?")
            values.append(preferred_color)
        if username is not None:
            fields.append("username = ?")
            values.append(username)
        if minecraft_uuid is not None:
            fields.append("minecraft_uuid = ?")
            values.append(minecraft_uuid)
        if discord_username is not None:
            fields.append("discord_username = ?")
            values.append(discord_username)
        if guild is not None:
            fields.append("guild = ?")
            values.append(guild)

        if fields:
            query = f'UPDATE Users SET {", ".join(fields)} WHERE id = ?'
            values.append(user_id)
            self.connection.execute(query, values)
            self.connection.commit()

    def unlink_user(self, user_id):
        query = 'UPDATE Users SET minecraft_uuid = ?, guild = ? WHERE id = ?;'
        self.connection.execute(query, (None, None, user_id,))
        self.connection.commit()
    def delete_user(self, user_id: int):
        query = 'DELETE FROM Users WHERE id = ?;'
        self.connection.execute(query, (user_id,))
        self.connection.commit()

    def close(self):
        self.connection.close()


