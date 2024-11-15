from flask_mail import Mail, Message

mail = Mail()

def check_inventory():
    from main import mongo,mail
    low_stock_items = list(mongo.db.inventory_items.find({"quantity":{"$lt":10}}))
    for item in low_stock_items:
        msg = Message(
            f"Low Stock Alert : {item['name']}",
            recipients=['admin@example.com'],
            body=f"Then item '{item['name']} is running low with only {item['quantity']} left in stock."
        )
        mail.send(msg)

