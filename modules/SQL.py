import os, sys
import sqlite3

SQL = None
sqlCursor = None

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def deleteTag( tag_id ):
	global SQL, sqlCursor
	query = ('DELETE FROM tags '
					'where tag_id == "{0}"').format( tag_id )
	sqlCursor.execute( query )
	SQL.commit()
	
def getTag( tag_id ):
	"""
	tag_id = (String) Hex of byteArray
	"""
	global SQL, sqlCursor
	d = sqlCursor.execute( 'SELECT * FROM tags WHERE tag_id LIKE (?)', (tag_id,) )
	return d.fetchone()
	
def writeTag(entryDict):
    '''
    entryDict = {"tag_id": text, "name": text, "date": text, "time": text, "audio_file": text}
    '''
    global SQL, sqlCursor
    
    # Attempt to update an existing row
    update_query = ('UPDATE tags SET '
                    'name = :name, date = :date, time = :time, audio_file = :audio_file '
                    'WHERE tag_id = :tag_id')
    sqlCursor.execute(update_query, entryDict)
    
    if sqlCursor.rowcount == 0:
        # If no rows were updated, this tag_id does not exist, so insert a new row
        insert_query = ('INSERT INTO tags '
                        '(tag_id, name, date, time, audio_file) '
                        'VALUES (:tag_id, :name, :date, :time, :audio_file)')
        sqlCursor.execute(insert_query, entryDict)
    
    SQL.commit()

	
def getDatabasePath ( defaultPath = './modules/' ):
	global SQL, sqlCursor
	path = os.path.realpath( defaultPath )
	if not os.path.isdir( path ):
		defaultPath = os.path.realpath( os.path.dirname(sys.argv[0]) )
		path = os.path.join( defaultPath,'tags' )
	return os.path.join( path, 'tags.db' )

def init():
	global SQL, sqlCursor
	DATABASE_PATH = getDatabasePath()
	SQL = sqlite3.connect( DATABASE_PATH, check_same_thread=False )
	SQL.row_factory = dict_factory
	sqlCursor = SQL.cursor()

	#Create database table
	sqlCursor.execute( 'CREATE TABLE IF NOT EXISTS tags ' 
									'(id INTEGER PRIMARY KEY AUTOINCREMENT '
									'UNIQUE, tag_id TEXT, name TEXT, '
									'date TEXT, time TEXT, audio_file TEXT)')
	SQL.commit()