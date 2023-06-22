# # Reset auto increment of PlayerID in Player Entity
# def reset_auto_increment(x: int):
#     # Connect to host root server on computer 
#     db = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         passwd="password",
#         database="MainDB"
#     )
#     # Setup cursor to execute SQL commands on DB
#     mycursor = db.cursor()

#     mycursor.execute(f"""
#     ALTER TABLE Player 
#     AUTO_INCREMENT = {x};
#     """)
#     db.commit()
#     db.close()

# reset_auto_increment(3)