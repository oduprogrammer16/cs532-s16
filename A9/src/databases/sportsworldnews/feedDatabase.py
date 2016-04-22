import sqlite3

# Used to manage the database for the feed
class FeedDatabase:
	def __init__(self,databaseName):
		self.conn = sqlite3.connect(databaseName)
		self.conn.execute("CREATE TABLE IF NOT EXISTS feeds(title,description,actualcategory,guid,isTrainingData)") # Table containing all the feeds, their title, their description and actual category
		self.conn.execute("CREATE TABLE IF NOT EXISTS feature_category_combinations(feature,category,count)")
		self.conn.execute("CREATE TABLE IF NOT EXISTS category_counts(category,count)")
		self.conn.execute("CREATE TABLE IF NOT EXISTS predictedEntries(guid,predictedCategory,fprob,cprob)")

	def add_feed_element(self,title,guid,description,actualcategory):
		self.conn.execute('''INSERT INTO feeds VALUES (?,?,?,?,?)''',(title,description,actualcategory,guid,0))		
		self.conn.commit()

	def change_classified(self,guid,classified=True):
		if classified:
			self.conn.execute("UPDATE feeds SET isTrainingData=1 WHERE guid='{0}'".format(guid))
		else:
			self.conn.execute("UPDATE feeds SET isTrainingData=0 WHERE guid='{0}'".format(guid))
		self.conn.commit()

	def add_predictedEntry(self,guid,predictedCategory,fprob,cprob):
		self.conn.execute('''INSERT INTO predictedEntries VALUES (?,?,?,?)'''(guid,predictedCategory,fprob,cprob))
		self.conn.commit()

	def get_unpredicted_entries(self):
		result = self.conn.execute("SELECT * FROM feeds WHERE isTrainingData=0")
		return [{'guid':row[3],'description':row[1]} for row in result]

	def close_database(self):
		self.conn.close()
